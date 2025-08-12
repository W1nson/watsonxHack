//
//  PaymentCardView.swift
//  iOS
//
//  Created by Jessica Trans on 8/11/25.
//

import SwiftUI

struct PaymentCardView: View {
    let subscription: Subscription
    
    func getSubscriptionColor() -> Color {
        let subscription = subscription.name.lowercased()
        if subscription.contains("spotify") {
            return Color.spotifyGreen
        } else if subscription.contains("netflix") {
            return Color.netflixRed
        } else if subscription.contains("playstation") {
            return Color.playstationBlue
        } else {
            return Color.customGray
        }
    }
    
    var body: some View {
        VStack {
            VStack {
                if subscription.name.lowercased().contains("view all") {
                    HStack {
                        Text("View All")
                            .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                        Image("arrow_forward")
                    }
                    .foregroundColor(Color.customPurple)
                } else {
                    ZStack(alignment: .bottom) {
                        RoundedRectangle(cornerRadius: 8)
                            .fill(getSubscriptionColor())
                            .frame(width: 110, height: 40)
                            .padding(.bottom, 20)
                        subscription.icon
                    }
                    
                    Text(subscription.name)
                        .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    Text(subscription.amount)
                        .font(.setCustom(fontStyle: .body, fontWeight: .semibold))
                    Divider()
                        .background(Color.divider)
                    Text(subscription.date)
                        .font(.setCustom(fontStyle: .caption, fontWeight: .medium))
                        .foregroundColor(Color.customDarkGray)
                }
            }
            .padding(10)
        }
        .frame(width: 124, height: 152)
        .padding(2)
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

#Preview {
    PaymentCardView(subscription: subscriptions[0])
}
