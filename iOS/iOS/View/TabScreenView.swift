//
//  TabScreenView.swift
//  iOS
//
//  Created by Jessica Trans on 8/3/25.
//

import SwiftUI

struct TabScreenView: View {
    enum Tab: Hashable {
        case tab1, tab2, tab3
    }
    @State private var selectedTab: Tab = .tab2
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // replace with actual screen views
            Text("Tab1")
                .tabItem {
                    Image(systemName: "message")
                    Text("Tab1")
                }
            Text("Tab2")
                .tabItem {
                    Image(systemName: "person")
                    Text("Tab2")
                }
            Text("Tab3")
                .tabItem {
                    Image(systemName: "person.crop.circle")
                    Text("Tab3")
                }
        }
//        .accentColor(Color(.red))
    }
}

#Preview {
    TabScreenView()
}
