//
//  TransactionsView.swift
//  iOS
//
//  Created by Jessica Trans on 8/11/25.
//

import SwiftUI

struct TransactionsView: View {
    var body: some View {
        VStack(alignment: .leading) {
            VStack {
                HStack {
                    Image("T-mobile")
                        .foregroundColor(Color.customBlack)
                    VStack(alignment: .leading) {
                        Text("T-Mobile Go5G Plus")
                            .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                        Text("March 16 · Pending")
                            .font(.setCustom(fontStyle: .caption, fontWeight: .medium))
                            .foregroundColor(Color.customDarkGray)
                    }
                    
                    Spacer()
                    Text("$150.00")
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                        .foregroundColor(Color.notifyRed)
                }
                .padding(.vertical, 10)
                
                Divider()
                    .padding(.leading, 40)
                
                HStack {
                    Image("hello_fresh")
                        .foregroundColor(Color.customBlack)
                    VStack(alignment: .leading) {
                        Text("HelloFresh Meal Kit")
                            .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                        Text("March 15")
                            .font(.setCustom(fontStyle: .caption, fontWeight: .medium))
                            .foregroundColor(Color.customDarkGray)
                    }
                    
                    Spacer()
                    Text("$85.93")
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                        .foregroundColor(Color.notifyRed)
                }
                .padding(.vertical, 10)
                
                Divider()
                    .padding(.leading, 40)
                
                HStack {
                    Image("icloud")
                        .foregroundColor(Color.customBlack)
                    VStack(alignment: .leading) {
                        Text("iCloud+ 200GB")
                            .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                        Text("March 14")
                            .font(.setCustom(fontStyle: .caption, fontWeight: .medium))
                            .foregroundColor(Color.customDarkGray)
                    }
                    
                    Spacer()
                    Text("$2.99")
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                        .foregroundColor(Color.notifyRed)
                }
                .padding(.vertical, 10)
                
                Divider()
                    .padding(.leading, 40)
                
                HStack {
                    Image("hello_fresh")
                        .foregroundColor(Color.customBlack)
                    VStack(alignment: .leading) {
                        Text("HelloFresh Meal Kit")
                            .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                        Text("March 8")
                            .font(.setCustom(fontStyle: .caption, fontWeight: .medium))
                            .foregroundColor(Color.customDarkGray)
                    }
                    
                    Spacer()
                    Text("$85.93")
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                        .foregroundColor(Color.notifyRed)
                }
                .padding(.vertical, 10)
            }

            Button {
                
            } label: {
                Text("View More")
                    .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    .foregroundStyle(Color.customPurple)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 10)
            .background(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(Color.customPurple, lineWidth: 1)
            )
            .padding(.top, 20)
        }
        .padding()
        .background(Color.white)
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

#Preview {
    TransactionsView()
}
