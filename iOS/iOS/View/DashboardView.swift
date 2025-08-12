//
//  DashboardView.swift
//  iOS
//
//  Created by Jessica Trans on 8/7/25.
//

import SwiftUI

struct DashboardView: View {
    let headerHeight: CGFloat = UIScreen.main.bounds.height / 5
    let maxHeaderExtension: CGFloat = 100
    
    var body: some View {
        ScrollView {
            ZStack(alignment: .top) {
                GeometryReader { proxy in
                    Color.customPurple
                        .frame(height: self.calculateHeaderHeight(proxy: proxy))
                        .offset(y: self.calculateHeaderOffset(proxy: proxy))
                }
                .frame(height: headerHeight)
                
                VStack(spacing: 0) {
                    DashboardHeaderView()
                    SpendingCardView()
                        .padding()
                    HStack {
                        TitleLabelView(title: "Upcoming Payments")
                        Spacer()
                        HStack {
                            Text("View All")
                                .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                            Image("arrow_forward")
                        }
                        .foregroundColor(Color.customPurple)
                        
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 20)
                    
                    CardHorizontalScroll()
                    
                    TitleLabelView(title: "Subscriptions & Free Trials (\(subscriptions.count))")
                        .font(.setCustom(fontStyle: .title, fontWeight: .semibold))

                        .padding(.horizontal, 20)
                        .padding(.top, 20)
                    
                    SubscriptionView()
                        .padding()
                    
                    HStack {
                        TitleLabelView(title: "Linked Accounts")
                        Spacer()
                        HStack {
                            Image("directory_sync")
                            Text("Sync (1 min ago)")
                                .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                                .underline(true)
                        }
                        .foregroundColor(Color.customPurple)
                        
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 20)
                    
                    AccountsView()
                        .padding()

                    TitleLabelView(title: "Transactions")
                        .padding(.horizontal, 20)
                        .padding(.top, 20)
                    
                    TransactionsView()
                        .padding()
                    
                    // TODO: customize dashboard
                    CustomizeDashboardView()
                        .padding()
                }
            }
        }
        .safeAreaInset(edge: .top, spacing: 0) {
            Color.customPurple
                .ignoresSafeArea()
                .frame(height: 0)
        }
        .background(Color.customGray)
    }
    // Calculate the header's height based on scroll position.
    private func calculateHeaderHeight(proxy: GeometryProxy) -> CGFloat {
        let minY = proxy.frame(in: .global).minY
        let extendedHeight = headerHeight + minY
        let cappedHeight = min(extendedHeight, headerHeight + maxHeaderExtension)
        
        return max(headerHeight, cappedHeight)
    }

    // Calculate the header's vertical offset.
    private func calculateHeaderOffset(proxy: GeometryProxy) -> CGFloat {
        let minY = proxy.frame(in: .global).minY
        return minY > 0 ? -minY : 0
    }
}

struct TitleLabelView: View {
    let title: String
    var body: some View {
        HStack {
            Text(title)
                .font(.setCustom(fontStyle: .title, fontWeight: .semibold))
            Spacer()
        }
    }
}

struct CardHorizontalScroll: View {
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 10) {
                ForEach(subscriptions.prefix(4)) { subscription in
                    PaymentCardView(subscription: subscription)
                }
                
                if subscriptions.count > 4 {
                    let viewAllPayment = Subscription(name: "View All", amount: "", date: "", isFreeTrial: false, icon: Image(""))
                    PaymentCardView(subscription: viewAllPayment)
                }
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 15)
        }
    }
}

struct SubscriptionView: View {
    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                HStack(spacing: -7) {
                    ForEach(subscriptions.prefix(8).indices, id: \.self) { index in
                        subscriptions[index].icon
                            .clipShape(Circle())
                            .zIndex(Double(index))
                    }
                    Spacer()
                    
                    if subscriptions.count > 8 {
                        Text("+\(subscriptions.count - 8)")
                            .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                            .padding(.trailing, 25)
                    }
                    
                    Image("arrow_right")
                        .foregroundColor(Color.customDarkGray)
                }
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

struct CustomizeDashboardView: View {
    var body: some View {
        VStack(alignment: .center) {
            HStack {
                Spacer()
                Text("Customize Dashboard")
                    .font(.setCustom(fontStyle: .body, fontWeight: .medium))
                    .foregroundColor(Color.customPurple)
                
                Spacer()
            }
            .padding()
        }
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

#Preview {
    DashboardView()
}
