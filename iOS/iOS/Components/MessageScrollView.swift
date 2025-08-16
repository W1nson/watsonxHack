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
    var isSug: Bool = false
}

struct MessageScrollView: View {
    let messages: [ChatMessage]
    let isLoading: Bool
    let onSuggestionTap: ((String) -> Void)?
    
    init(
        messages: [ChatMessage],
        isLoading: Bool,
        onSuggestionTap: ((String) -> Void)? = nil
    ) {
        self.messages = messages
        self.isLoading = isLoading
        self.onSuggestionTap = onSuggestionTap
    }
    
    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 12) {
                    ForEach(messages.indices, id: \.self) { index in
                        let previousMessage = index > 0 ? messages[index - 1] : nil
                        MessageRowView(message: messages[index], previousMessage: previousMessage, onSuggestionTap: onSuggestionTap)
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
    let onSuggestionTap: ((String) -> Void)?
    
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
                    if message.isSug {
                        Button(action: { onSuggestionTap?(message.text) }) {
                            Markdown(message.text)
                                .markdownBlockStyle(\.paragraph) {
                                    configuration in
                                    VStack {
                                        configuration.label
                                    }
                                    .markdownTextStyle {
                                          FontSize(14)
                                        }
                                    .padding(.vertical, 8)
                                    .padding(.horizontal, 16)
                                    .cornerRadius(24)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 24)
                                            .stroke(Color.customPurple, lineWidth: 1)
                                    )
                                    .foregroundColor(Color.customPurple)
                                }
                        }
                    }
                    
                    else if message.isRec {
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
                                    .markdownTextStyle {
                                          FontSize(14)
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
                                .padding(.bottom, 2)
                            Markdown(message.text)
                                .markdownBlockStyle(\.listItem) { configuration in
                                    configuration.label
                                        .padding(.leading, -15)
                                        .padding(.bottom, 8)
                                }
                            
                                .markdownBlockStyle(\.paragraph) { configuration in
                                    configuration.label
                                        .markdownTextStyle {
                                          FontSize(14)
                                        }
                                }
                                .padding(.trailing, 40)
                                .lineSpacing(3)

                        }
                    }
                }
                else {
                    Markdown(message.text)
                        .markdownBlockStyle(\.paragraph) { configuration in
                            configuration.label
                                .markdownTextStyle {
                                    FontSize(14)
                                }
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
        
        let markdownString2 = """
        Hi James, based on your current subscription list, here are some tips to save approximately $3,300 a year:
                  
        * **Switch to Netflix Standard with Ads** ($6.99/month) as it's much cheaper than your current plan, though it includes ads and Full HD resolution.
        * **Consider switching your Spotify Premium to a free plan with occasional ads** to save around $143.88 annually.
        * **Explore the Google One Family plan** for better value if multiple users are involved, potentially costing more upfront but offering shared benefits.
        * **Keep an eye out for annual discounts or free trials** on your PlayStation Plus, which could save you $50 a year.
        * **Evaluate your Kindle Unlimited usage and consider using your local library for free e-books and audiobooks** to save approximately $143.88 annually.
        * **Plan your meals and shop for groceries** instead of using HelloFresh, which could save you a significant amount based on your usage.
             
        These changes can help you optimize your subscriptions based on your usage patterns and preferences. Do you want to prioritize reducing costs, simplifying management, or hunting for better deals?
        """

        let sampleMessages = [
            ChatMessage(text: "Hi Alice, Here are some things I can help with:", isUser: false, timestamp: Date().addingTimeInterval(-3600), avatar: "Avatar-jarvis"),
            ChatMessage(text: "Recommend Subscriptions", isUser: false, timestamp: Date().addingTimeInterval(-300), avatar: "", isSug: true),
            ChatMessage(text: "Ask About Subscriptions", isUser: false, timestamp: Date().addingTimeInterval(-300), avatar: "", isSug: true),
            ChatMessage(text: "Compare Subscriptions", isUser: false, timestamp: Date().addingTimeInterval(-300), avatar: "", isSug: true),
            ChatMessage(text: "Save Money", isUser: false, timestamp: Date().addingTimeInterval(-300), avatar: "", isSug: true),
            ChatMessage(text: greetingString, isUser: false, timestamp: Date().addingTimeInterval(-120), avatar: "Avatar-jarvis"),
            ChatMessage(text: recommandatiaons, isUser: false, timestamp: Date().addingTimeInterval(-90), avatar: "", isRec: true),
            ChatMessage(text: "Can you tell me how to budget?", isUser: true, timestamp: Date().addingTimeInterval(-60), avatar: ""),
//            ChatMessage(text: markdownString2, isUser: false, timestamp: Date(), avatar: "Avatar-jarvis"),
            ChatMessage(text: markdownString, isUser: false, timestamp: Date(), avatar: "Avatar-jarvis")
        ]
        
        MessageScrollView(messages: sampleMessages, isLoading: false)
            .previewLayout(.sizeThatFits)
    }
}
