//
//  ChatView.swift
//  iOS
//
//  Created by Jessica Trans on 8/5/25.
//

import SwiftUI
import MarkdownUI

struct ChatRequest: Codable {
    let user_input: String
    let user_id: String
}

struct ChatResponse: Codable {
    let response: String
    let recommendations: [String]
    let answer: [String]
    let follow_up: [String]
}

struct ChatView: View {
    @StateObject private var viewModel = ChatViewModel()
    @Binding var showingSheet: Bool

    var body: some View {
        ChatHeaderTitleView(showingSheet: $showingSheet)
        
        VStack {
            MessageScrollView(
                messages: viewModel.messages,
                isLoading: viewModel.isLoading,
                onSuggestionTap: { text in viewModel.onSuggestionTap(text: text) }
            )
            Divider()
            InputView(viewModel: viewModel)
        }
    }
}

struct InputView: View {
    @ObservedObject var viewModel: ChatViewModel
    
    var body: some View {
        HStack {
            ZStack(alignment: .leading) {
                RoundedRectangle(cornerRadius: 24)
                    .fill(Color.customGray)
                
                HStack(spacing: 2) {
                    TextField("Message", text: $viewModel.inputText)
                        .font(.setCustom(fontStyle: .body, fontWeight: .regular))
                        .padding(9)
                        .padding(.horizontal, 4)
                    
                    if !viewModel.inputText.trimmingCharacters(in: .whitespaces).isEmpty {
                        Button(action: viewModel.sendMessage) {
                            Image("arrow_circle_up")
                        }
                        .padding(.trailing, 10)
                    }
                }
            }
            .fixedSize(horizontal: false, vertical: true)
            
            Button(action: {
                // TODO: Handle microphone action
            }) {
                Image("mic")
            }
            .padding(.horizontal, 8)
        }
        .padding()
    }
}

#Preview {
    @Previewable @State var isSheetPresented = false
    ChatView(showingSheet: $isSheetPresented)
}
