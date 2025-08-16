//
//  DashboardHeaderView.swift
//  iOS
//
//  Created by Jessica Trans on 8/7/25.
//

import SwiftUI

struct DashboardHeaderView: View {
    var body: some View {
        HeaderContent()
    }
}

private struct HeaderContent: View {
    var body: some View {
        VStack {
            IconView()
            TitleView()
            Spacer()
        }
        .foregroundColor(.white)
        .padding(.horizontal, 3)
    }
}

struct TitleView: View {
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text("Good Morning")
                    .font(.setCustom(fontStyle: .largeTitle, fontWeight: .semibold))
                    .padding(.bottom, 0.5)
                Text(Date.now, style: .date)
                    .font(.setCustom(fontStyle: .title2, fontWeight: .medium))
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.horizontal)
    }
}

struct IconView: View {
    var body: some View {
        HStack {
            Spacer()
            HStack(spacing: 16) {
                Image("account_circle")
                    .resizable()
                    .frame(width: 24, height: 24)
                    .padding(.trailing, 5)

                ZStack(alignment: .topTrailing) {
                    Image("notifications")
                        .resizable()
                        .frame(width: 24, height: 24)
                    
                    // The badge view
                    Text("4")
                        .font(.setCustom(fontStyle: .caption, fontWeight: .medium))
                        .foregroundColor(.white)
                        .padding(5)
                        .background(Color.notifyRed)
                        .clipShape(Circle())
                        .offset(x: 4, y: -8)
                }
            }
        }
        .padding(.horizontal)
    }
}

#Preview {
    DashboardHeaderView()
}
