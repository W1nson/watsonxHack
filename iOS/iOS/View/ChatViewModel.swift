//
//  ChatViewModel.swift
//  iOS
//
//  Created by Winson Chen on 8/4/25.
//


import Foundation
import Combine
import MarkdownUI

struct Message: Codable {
    let role: String
    let content: String
}

struct ChatAPIResponseString: Codable { let response: Message }
struct ChatAPIResponseArray: Codable { let response: [Message] }


class ChatViewModel: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var inputText: String = ""
    @Published var isLoading = false

    private let endpoint = "http://localhost:8000/chat"

    func sendMessage() {
        let trimmed = inputText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return }

        let userMessage = ChatMessage(text: trimmed, isUser: true, timestamp: Date(), avatar: "person.circle.fill")
        messages.append(userMessage)
        inputText = ""
        isLoading = true

        Task {
            do {
                let aiReply = try await fetchReply(for: trimmed)
                DispatchQueue.main.async {
                    self.isLoading = false
                }
            } catch {
                DispatchQueue.main.async {
                    self.messages.append(ChatMessage(text: "Error: \(error.localizedDescription)", isUser: false, timestamp: Date(), avatar: "brain.head.profile"))
                    self.isLoading = false
                }
            }
        }
    }

    private func fetchReply(for userInput: String, userId: String = "2") async throws -> String {
        // Building the backend URL
        guard let url = URL(string: endpoint) else { throw URLError(.badURL) }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")


        let body = try JSONEncoder().encode(ChatRequest(user_input: userInput, user_id: userId))
        request.httpBody = body

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }

        let decoder = JSONDecoder()
        let res = try decoder.decode(ChatAPIResponseArray.self, from: data)
        var replyText = ""
        for message in res.response {
            replyText += message.content
            let currentReplyText = replyText
            DispatchQueue.main.async {
                if let last = self.messages.last, !last.isUser {
                    self.messages[self.messages.count - 1] = ChatMessage(
                        text: currentReplyText,
                        isUser: false,
                        timestamp: self.messages[self.messages.count - 1].timestamp,
                        avatar: self.messages[self.messages.count - 1].avatar
                    )
                } else {
                    self.messages.append(ChatMessage(text: currentReplyText, isUser: false, timestamp: Date(), avatar: "brain.head.profile"))
                }
            }
        }

        return replyText
    }
}
