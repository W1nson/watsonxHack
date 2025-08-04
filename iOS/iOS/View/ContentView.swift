//
//  ContentView.swift
//  iOS
//
//  Created by Jessica Trans on 8/3/25.
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
                                            .foregroundColor(message.isUser ? .blue : .gray)

                                        VStack(alignment: .leading) {
                                            Markdown(message.text)
                                                .padding()
                                                .background(message.isUser ? Color.blue.opacity(0.2) : Color.gray.opacity(0.2))
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
                .onChange(of: viewModel.messages.count) { _ in
                    withAnimation {
                        proxy.scrollTo(viewModel.messages.last?.id, anchor: .bottom)
                    }
                }
            }

            Divider()

            HStack {
                TextField("Type a message...", text: $viewModel.inputText)
                    .textFieldStyle(RoundedBorderTextFieldStyle())

                Button(action: {
                    viewModel.sendMessage()
                }) {
                    Image(systemName: "arrow.up.circle.fill")
                        .font(.title2)
                }
                .disabled(viewModel.inputText.trimmingCharacters(in: .whitespaces).isEmpty)
            }
            .padding()
        }
    }
}


struct ContentView: View {
    var body: some View {
        TabScreenView() 
    }
    
    // TODO: Connect API Endpoints

    
    
    
    
}

#Preview {
//    ContentView()
    ChatView()
}
