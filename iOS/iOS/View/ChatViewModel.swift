//
//  ChatViewModel.swift
//  iOS
//
//  Created by Winson Chen on 8/4/25.
//


import Foundation
import Combine
import MarkdownUI

private let recommendationsPrefix = "__RECOMMENDATIONS__:"

struct ChatAPIMessage: Codable {
    let role: String
    let content: String
}

struct ChatAPIResponse: Codable {
    let response: [ChatAPIMessage]
    let recommendations: [String]
    let answer: [String]
    let follow_up: [String]
}


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
        let api = try decoder.decode(ChatAPIResponse.self, from: data)
        
        print(api.recommendations)
        // 1) ANSWER bubble (plain text)
        var answerText: String? = nil
        if !api.answer.isEmpty {
            answerText = api.answer.joined(separator: " ")
//        } else if let lastAssistant = api.response.last(where: { $0.role.lowercased() == "assistant" }) {
//            answerText = lastAssistant.content
        }
        if let answerText {
            DispatchQueue.main.async {
                self.messages.append(ChatMessage(text: answerText, isUser: false, timestamp: Date(), avatar: "Avatar-jarvis"))
            }
        }

        // 2) RECOMMENDATIONS bubble (tagged for button UI)
        if !api.recommendations.isEmpty {
            let recs = api.recommendations
            for rec in recs {
                print("rec: \(rec)")
                DispatchQueue.main.async {
                    self.messages.append(ChatMessage(text: rec, isUser: false, timestamp: Date(), avatar: "Avatar-jarvis", isRec: true))
                }
            }
            
            
        }

        // 3) FOLLOW-UP bubble (plain text)
        if !api.follow_up.isEmpty {
//            let follows = api.follow_up
            let followText = api.follow_up.joined(separator: " ")
            DispatchQueue.main.async {
                self.messages.append(ChatMessage(text: followText, isUser: false, timestamp: Date(), avatar: "Avatar-jarvis"))
            }
        }

        // Return last non-empty piece for testing
        return self.messages.last?.text ?? ""
    }
}


