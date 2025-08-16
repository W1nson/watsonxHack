//
//  TransactionsView.swift
//  iOS
//
//  Created by Jessica Trans on 8/11/25.
//

import SwiftUI

struct TransactionRow: View {
    let imageName: String
    let title: String
    let date: String
    let amount: String
    let isPending: Bool
    
    var body: some View {
        HStack {
            Image(imageName)
                .resizable()
                .frame(width: 40, height: 40)
                .padding(.trailing, 5)
            VStack(alignment: .leading, spacing: 5) {
                Text(title)
                    .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    .foregroundColor(Color.textPrimary)
                Text(isPending ? "\(date) · Pending" : date)
                    .font(.setCustom(fontStyle: .caption, fontWeight: .medium))
                    .foregroundColor(.customDarkGray)
            }
            
            Spacer()
            
            Text(amount)
                .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                .foregroundColor(.notifyRed)
        }
        .padding(.vertical, 10)
    }
}

struct TransactionsView: View {
    var body: some View {
        VStack(alignment: .leading) {
            VStack(spacing: 3) {
                TransactionRow(
                    imageName: "T-mobile",
                    title: "T-Mobile Go5G Plus",
                    date: "August 16",
                    amount: "$150.00",
                    isPending: true
                )
                
                Divider()
                    .padding(.leading, 50)

                TransactionRow(
                    imageName: "hello_fresh",
                    title: "HelloFresh Meal Kit",
                    date: "August 15",
                    amount: "$85.93",
                    isPending: false
                )
                
                Divider()
                    .padding(.leading, 50)

                TransactionRow(
                    imageName: "icloud",
                    title: "iCloud+ 200GB",
                    date: "August 14",
                    amount: "$2.99",
                    isPending: false
                )
                
                Divider()
                    .padding(.leading, 50)

                TransactionRow(
                    imageName: "hello_fresh",
                    title: "HelloFresh Meal Kit",
                    date: "August 8",
                    amount: "$85.93",
                    isPending: false
                )
                
                Divider()
                    .padding(.leading, 50)
            }
            
            Button {
                // Action for viewing more transactions
            } label: {
                Text("View More")
                    .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    .foregroundStyle(Color.customPurple)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 14)
            .background(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(Color.customPurple, lineWidth: 1)
            )
            .padding(.top, 5)
        }
        .padding()
        .padding(.top, -5)
        .background(.white)
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.03), radius: 5, x: 0, y: 2)
    }
}

#Preview {
    TransactionsView()
}
