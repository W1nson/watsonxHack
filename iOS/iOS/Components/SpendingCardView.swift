//
//  SpendingCardView.swift
//  iOS
//
//  Created by Jessica Trans on 8/11/25.
//

import SwiftUI

struct SpendingCardView: View {
    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                Text("This Month's Spending")
                    .font(.setCustom(fontStyle: .title, fontWeight: .semibold))
                Spacer()
                Image("arrow_right")
                    .foregroundColor(Color.customDarkGray)
            }
            .padding(.bottom, 10)
            HStack {
                VStack(alignment: .leading) {
                    Text("Spent")
                        .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                        .foregroundStyle(Color.customDarkGray)
                        .padding(.bottom, -3)
                    Text("$432.77")
                        .font(.setCustom(fontStyle: .headline, fontWeight: .semibold))
                }
                Spacer()
                Divider()
                    .frame(height: 50)
                    .padding(.trailing, 10)
                VStack(alignment: .leading) {
                    Text("Upcoming")
                        .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                        .foregroundStyle(Color.customDarkGray)
                        .padding(.bottom, -3)
                    Text("$139.69")
                        .font(.setCustom(fontStyle: .headline, fontWeight: .semibold))
                }
                Spacer()
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(16)
        .shadow(radius: 2)
    }
}

#Preview {
    SpendingCardView()
}
