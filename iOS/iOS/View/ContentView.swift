//
//  ContentView.swift
//  iOS
//
//  Created by Jessica Trans on 8/3/25.
//

import SwiftUI

struct ContentView: View {
    @State private var showingSheet = false

    var body: some View {
        ZStack {
            DashboardView()
    
            ChatButtonView(showingSheet: $showingSheet)
                .sheet(isPresented: $showingSheet) {
                    ChatView(showingSheet: $showingSheet)
                        .presentationCornerRadius(25)
                }
        }
    }
}

#Preview {
    ContentView()
}
