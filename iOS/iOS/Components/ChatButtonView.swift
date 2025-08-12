//
//  ChatButtonView.swift
//  iOS
//
//  Created by Jessica Trans on 8/9/25.
//

import SwiftUI

struct ChatButtonView: View {
    @Binding var showingSheet: Bool

    var body: some View {
        VStack {
            Spacer()
            HStack {
                Spacer()
                Button(action: {
                    showingSheet.toggle()
                }) {
                    Image("ChatButton")
                }
                .padding(.trailing, 30)
                .padding(.bottom, 10)
            }
        }
    }
}

#Preview {
    @Previewable @State var isSheetPresented = false
    ChatButtonView(showingSheet: $isSheetPresented)
}
