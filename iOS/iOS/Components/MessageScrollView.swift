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
    let avatar: String
    var isRec: Bool = false
}

struct MessageScrollView: View {
    let messages: [ChatMessage]
    let isLoading: Bool
    
    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 12) {
                    ForEach(messages.indices, id: \.self) { index in
                        let previousMessage = index > 0 ? messages[index - 1] : nil
                        MessageRowView(message: messages[index], previousMessage: previousMessage)
                    }

                    if isLoading {
                        HStack {
                            ProgressView()
                            Text("Thinking...")
                                .font(.setCustom(fontStyle: .body, fontWeight: .regular))
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
    let previousMessage: ChatMessage?
    
    // Create a date formatter to display the date
    private let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .none
        formatter.doesRelativeDateFormatting = true
        return formatter
    }()
    
    var body: some View {
        VStack(alignment: message.isUser ? .trailing : .leading) {
            
            // Conditionally display the date if it's a new day
            if shouldShowDate(for: message, previous: previousMessage) {
                Text(dateFormatter.string(from: message.timestamp))
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity)
            }
            
            HStack(alignment: .top, spacing: 8) {
                if !message.isUser {
                    if message.isRec {
                        VStack(alignment: .leading) {
                            Markdown(message.text)
                                .markdownBlockStyle(\.paragraph) { configuration in
                                    VStack {
                                        HStack {
                                            configuration.label
                                            // TODO: add icon based on tips
                                            Spacer()
                                            //                                        Image("netflix")
                                            //                                            .padding(.leading, 10)
                                        }
                                    }
                                    .padding()
                                    .cornerRadius(10)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 10)
                                            .stroke(Color.customPurple, lineWidth: 1)
                                    )
                                    .foregroundColor(Color.customPurple)
                                }
                                .padding(.top, 5)
                        }
                    }
                    else {
                        VStack(alignment: .leading) {
                            Image(message.avatar)
                            Markdown(message.text)
                                .markdownBlockStyle(\.paragraph) { configuration in
                                    configuration.label
                                }
                        }
                    }
                }
                else {
                    Markdown(message.text)
                        .markdownBlockStyle(\.paragraph) { configuration in
                            configuration.label
//                                .font(.setCustom(fontStyle: .body, fontWeight: .regular))
                                .foregroundColor(.white)
                                .padding(.horizontal)
                                .padding(.vertical, 10)
                                .background(Color.messageBubble)
                                .cornerRadius(20)
                        }
                        .padding(.vertical, 20)
                }
            }
            .frame(maxWidth: .infinity, alignment: message.isUser ? .trailing : .leading)
        }
    }
    
    private func shouldShowDate(for current: ChatMessage, previous: ChatMessage?) -> Bool {
        guard let previous = previous else {
            return true
        }
        let calendar = Calendar.current
        return !calendar.isDate(current.timestamp, inSameDayAs: previous.timestamp)
    }
}

//#Preview {
//    @Previewable @StateObject var viewModel = ChatViewModel()
//    MessageScrollView(messages: viewModel.messages, isLoading: viewModel.isLoading)
//}

// MARK: - Preview
struct MessageScrollView_Previews: PreviewProvider {
    static var previews: some View {
        let greetingString = """
            Here are some tips to save **$1,200** a year:
            """
        let recommandatiaons = "Cancel **Chess.com Diamond subscription** that was not used in the past 6 months."
        
        let markdownString = """
            Based on the provided data and web search, here is your personalized budgeting analysis, Alice:
            1. **Usage Analysis**
               - Netflix: The subscription was cancelled on 01/08/2023, indicating it was not actively used after cancellation.
            2. **Cost Efficiency Evaluation**
               - The most expensive subscription listed is Adobe Creative Cloud at $54.99.
               - Netflix, while cancelled, was $6.99 for the 'Standard with Ads' tier, which might have been moderately priced for its features at the time.
            3. **Cheaper Alternatives**
               - For streaming, there are cheaper alternatives:
                 - Disney+: Starts at $7.99/month or $79.99/year.
                 - HBO Max: $9.99/month.
                 - Paramount+: $4.99/month for the Essential plan.
               - These are basic plans and might not offer the exact same features as Netflix.
            4. **Cancellation Suggestions**
               - Netflix: You've already cancelled this, which is a great step.
               - For Adobe Creative Cloud, if you're not actively using it and considering creative software, it might be worth evaluating if a cheaper, project-based plan or a different service (like those listed in cheaper alternatives) suits your current needs.
            ...
               - Consider Replacing: Netflix, based on the available cheaper streaming alternatives listed if you wish to have a streaming service.
               - Estimated savings are difficult to quantify without knowing your exact usage but could be around $15-$60 monthly, depending on the decisions made.
            """

        let sampleMessages = [
            ChatMessage(text: greetingString, isUser: false, timestamp: Date().addingTimeInterval(-120), avatar: "Avatar-jarvis"),
            ChatMessage(text: recommandatiaons, isUser: false, timestamp: Date().addingTimeInterval(-90), avatar: "", isRec: true),
            ChatMessage(text: "Can you tell me how to budget?", isUser: true, timestamp: Date().addingTimeInterval(-60), avatar: ""),
            ChatMessage(text: markdownString, isUser: false, timestamp: Date(), avatar: "Avatar-jarvis")
        ]
        
        MessageScrollView(messages: sampleMessages, isLoading: false)
            .previewLayout(.sizeThatFits)
    }
}
