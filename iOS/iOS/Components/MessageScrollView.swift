//
//  MessageScrollView.swift
//  iOS
//
//  Created by Jessica Trans on 8/10/25.
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

struct MessageScrollView: View {
    let messages: [ChatMessage]
    let isLoading: Bool
    
    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 12) {
                    ForEach(messages) { message in
                        MessageRowView(message: message)
                    }

                    if isLoading {
                        HStack {
                            ProgressView()
                            Text("Thinking...")
                        }
                    }
                }
                .padding()
            }
            .onChange(of: messages.count) {
                withAnimation {
                    proxy.scrollTo(messages.last?.id, anchor: .bottom)
                }
            }
        }
    }
}

struct MessageRowView: View {
    let message: ChatMessage
    
    var body: some View {
        HStack(alignment: .top) {
            if message.isUser {
                Spacer()
            }
            
            VStack(alignment: .leading, spacing: 4) {
                HStack(alignment: .top, spacing: 8) {
                    Image("Avatar-jarvis")
//                    Image(message.avatar)
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
            
            if !message.isUser {
                Spacer()
            }
        }
    }
}

//#Preview {
//    @Previewable @StateObject var viewModel = ChatViewModel()
//    MessageScrollView(messages: viewModel.messages, isLoading: viewModel.isLoading)
//}

// MARK: - Preview
struct MessageScrollView_Previews: PreviewProvider {
    static var previews: some View {
        // Create sample data to display in the preview
        let sampleMessages = [
            ChatMessage(text: "Hello, how can I help you today?", isUser: false, timestamp: Date().addingTimeInterval(-120), avatar: "Avatar-jarvis"),
            ChatMessage(text: "Can you tell me about SwiftUI?", isUser: true, timestamp: Date().addingTimeInterval(-60), avatar: "Avatar-user"),
            ChatMessage(text: "SwiftUI is a modern declarative UI framework for building apps on Apple platforms.", isUser: false, timestamp: Date(), avatar: "Avatar-jarvis")
        ]
        
        MessageScrollView(messages: sampleMessages, isLoading: false)
            .previewLayout(.sizeThatFits)
    }
}
