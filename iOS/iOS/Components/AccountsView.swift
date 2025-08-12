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
                HStack {
                    Image("account_balance")
                        .foregroundColor(Color.customBlack)
                        .padding(.trailing, 8)
                    Text("Checking (4)")
                        .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    Spacer()
                    Text("$67,564")
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                    Image("arrow_down")
                        .foregroundColor(Color.interactiveGray)
                }
                .padding(.vertical, 10)
                
                Divider()
                    .padding(.leading, 40)
                
                HStack {
                    Image("credit_card")
                        .foregroundColor(Color.customBlack)
                        .padding(.trailing, 8)
                    Text("Card Balance (6)")
                        .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    Spacer()
                    Text("$21,492")
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                    Image("arrow_down")
                        .foregroundColor(Color.interactiveGray)
                }
                .padding(.vertical, 5)
                
                Divider()
                    .padding(.leading, 40)

                HStack {
                    Image("savings")
                        .foregroundColor(Color.customBlack)
                        .padding(.trailing, 8)
                    Text("Savings (4)")
                        .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    Spacer()
                    Text("$162,965")
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                    Image("arrow_down")
                        .foregroundColor(Color.interactiveGray)
                }
                .padding(.vertical, 5)
                
                Divider()
                    .padding(.leading, 40)
                
                HStack {
                    Image("add_2")
                        .foregroundColor(Color.customBlack)
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
        .background(Color.white)
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

#Preview {
    AccountsView()
}
