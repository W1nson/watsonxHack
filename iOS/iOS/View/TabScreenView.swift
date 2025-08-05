//
//  TabScreenView.swift
//  iOS
//
//  Created by Jessica Trans on 8/3/25.
//

import SwiftUI

struct TabScreenView: View {
    enum Tab: Hashable {
            case dashboard, payments, analytics, transactions, jarvisAI
        }
    @State private var selectedTab: Tab = .jarvisAI
    @State private var isTapped = false

    var body: some View {
        // replace with actual screen views
        TabView(selection: $selectedTab) {
            Text("Dashboard Tab")
                .tabItem {
                    Image(selectedTab == .dashboard ? "dashboard-interactive" : "dashboardtest")
                    Text("Dashboard")
                }
                .tag(Tab.dashboard)
            Text("Payments Tab")
                .tabItem {
                    Image(selectedTab == .payments ? "payments-interactive" : "payments")
                    Text("Payments")
                }
                .tag(Tab.payments)

            Text("Analytics Tab")
                .tabItem {
                    Image(selectedTab == .analytics ? "analytics-interactive" : "analytics")
                    Text("Analytics")
                }
                .tag(Tab.analytics)

            Text("Transactions Tab")
                .tabItem {
                    Image(selectedTab == .transactions ? "transactions-interactive" : "transactions")
                    Text("Transactions")
                }
                .tag(Tab.transactions)

            ChatView()
                .tabItem {
                    Image(selectedTab == .jarvisAI ? "ai-interactive" : "ai")
                    Text("Jarvis")
                }
                .tag(Tab.jarvisAI)

        }
        .accentColor(Color(.purple))
    }
}

#Preview {
    TabScreenView()
}
