//
//  ChatView.swift
//  iOS
//
//  Created by Jessica Trans on 8/5/25.
//

import SwiftUI
import MarkdownUI

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
    let timestamp: Date
    let avatar: String // This can be a system image name or URL
}

struct ChatRequest: Codable {
    let user_input: String
    let user_id: String
}

struct ChatResponse: Codable {
    let response: String
}

struct ChatView: View {
    @StateObject private var viewModel = ChatViewModel()

    var body: some View {
        VStack {
            ScrollViewReader { proxy in
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 12) {
                        ForEach(viewModel.messages) { message in
                            HStack(alignment: .top) {
                                if message.isUser { Spacer() }

                                VStack(alignment: .leading, spacing: 4) {
                                    HStack(alignment: .top, spacing: 8) {
                                        Image(systemName: message.avatar)
                                            .resizable()
                                            .frame(width: 24, height: 24)
                                            .foregroundColor(message.isUser ? .purple : .gray)

                                        VStack(alignment: .leading) {
                                            Markdown(message.text)
                                                .padding()
                                                .background(message.isUser ? Color.purple.opacity(0.2) : Color.gray.opacity(0.2))
                                                .cornerRadius(10)

                                            Text(message.timestamp, style: .time)
                                                .font(.caption2)
                                                .foregroundColor(.secondary)
                                        }
                                    }
                                }

                                if !message.isUser { Spacer() }
                            }
                        }

                        if viewModel.isLoading {
                            HStack {
                                ProgressView()
                                Text("Thinking...")
                            }
                        }
                    }
                    .padding()
                }
                .onChange(of: viewModel.messages.count) {
                    withAnimation {
                        proxy.scrollTo(viewModel.messages.last?.id, anchor: .bottom)
                    }
                }
            }

            Divider()

            HStack {
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color(.systemGray5))
                        .cornerRadius(24)
                    HStack(spacing: 2) {
                        TextField("Message", text: $viewModel.inputText)
                            .padding(12)
                            .padding(.horizontal, 4)
                            .tint(.black)

                        if !viewModel.inputText.trimmingCharacters(in: .whitespaces).isEmpty {
                            Button(action: {
                                viewModel.sendMessage()
                            }) {
                                ZStack {
                                    Circle()
                                        .fill(Color.purple)

                                    Image(systemName: "arrow.up")
                                        .font(.caption)
                                        .fontWeight(.heavy)
                                        .foregroundColor(.white)
                                    }
                                    .frame(width: 24, height: 24)
                            }
                            .padding(.trailing, 10)
                        }
                    }
                }
                .fixedSize(horizontal: false, vertical: true)
                Button(action: {
                    // TODO
                }) {
                    Image(systemName: "microphone.fill")
                        .font(.title2)
                        .foregroundColor(Color(.darkGray))
                }
                .padding(.horizontal, 10)
            }
            .padding()
        }
    }
}

#Preview {
    ChatView()
}
