//
//  AccountsView.swift
//  iOS
//
//  Created by Jessica Trans on 8/11/25.
//


import SwiftUI

struct AccountsView: View {
    var body: some View {
        VStack(alignment: .leading) {
            VStack {
                AccountRowView(
                    imageName: "account_balance",
                    title: "Checking (4)",
                    amount: "$67,564"
                )
                Divider()
                    .padding(.leading, 40)

                AccountRowView(
                    imageName: "credit_card",
                    title: "Card Balance (6)",
                    amount: "$21,492"
                )
                Divider()
                    .padding(.leading, 40)

                AccountRowView(
                    imageName: "savings",
                    title: "Savings (4)",
                    amount: "$162,965"
                )
                Divider()
                    .padding(.leading, 40)

                HStack {
                    Image("add_2")
                        .foregroundColor(Color.interactiveGray)
                        .padding(.trailing, 8)
                    Text("Add Account")
                        .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    Spacer()
                }
                .padding(.vertical, 5)
                .foregroundColor(Color.interactiveGray)
            }
        }
        .padding()
        .padding(.vertical, -5)
        .background(Color.white)
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.03), radius: 5, x: 0, y: 2)
    }
}

struct AccountRowView: View {
    let imageName: String
    let title: String
    let amount: String

    var body: some View {
        HStack {
            Image(imageName)
                .foregroundColor(Color.customBlack)
                .padding(.trailing, 8)
            HStack {
                Text(title)
                    .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                Spacer()
                Text(amount)
                    .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
            }
            .foregroundColor(Color.textPrimary)

            Image("arrow_down")
                .foregroundColor(Color.interactiveGray)
        }
        .padding(.vertical, 7)
    }
}

#Preview {
    AccountsView()
}
