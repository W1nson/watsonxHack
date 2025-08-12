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
                    .frame(width: 30, height: 30)
                    .padding(.trailing, 5)
                Image("notifications")
                    .resizable()
                    .frame(width: 30, height: 30)
            }
        }
        .padding(.horizontal)
    }
}

#Preview {
    DashboardHeaderView()
}
