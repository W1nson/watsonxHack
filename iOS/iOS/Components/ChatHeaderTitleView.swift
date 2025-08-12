//
//  ChatHeaderTitleView.swift
//  iOS
//
//  Created by Jessica Trans on 8/6/25.
//

import SwiftUI

struct ChatHeaderTitleView: View {
    @Binding var showingSheet: Bool

    var body: some View {
        VStack {
            LinearGradient(
                gradient: Gradient(colors: [
                    Color(hex: "23607E"),
                    Color(hex: "3D2CA6"),
                    Color(hex: "981B62")
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing)
                    .edgesIgnoringSafeArea(.all)
                    .overlay(
                        ChatTitleView(showingSheet: $showingSheet)
                            .foregroundColor(.white)
                            .padding(.bottom, 6)
                    )
        }
        .frame(maxWidth: .infinity, maxHeight: 70)
    }
}

struct ChatTitleView: View {
    @Binding var showingSheet: Bool

    var body: some View {
        HStack {
            Button(action: {
                showingSheet.toggle()
            }) {
                Image(systemName: "xmark")
                    .fontWeight(.semibold)
                    .padding(.trailing, 16)
            }
            VStack(alignment: .leading) {
                Text("Jarvis AI")
                    .font(.setCustom(fontStyle: .title, fontWeight: .semibold))
                Text("with Watsonx AI")
                    .font(.setCustom(fontStyle: .title3, fontWeight: .medium))
            }
            Spacer()
            HStack {
                Image("search")
                    .padding(.trailing, 10)
                Image("more_vert")
            }
        }
        .padding(.horizontal, 20)
        .padding(.top, 20)
    }
}

#Preview {
    @Previewable @State var isSheetPresented = false
    ChatHeaderTitleView(showingSheet: $isSheetPresented)
}
