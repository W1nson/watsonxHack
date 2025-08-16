//
//  ColorExtensions.swift
//  iOS
//
//  Created by Jessica Trans on 8/10/25.
//

import SwiftUI

extension Color {
    static let customPurple = Color(hex: "#AB27FF")
    static let customGray = Color(hex: "#EEEDED")
    static let backgroundGray = Color(hex: "#EFEDF1")
    static let customDarkGray = Color(hex: "#727073")
//    static let customSpotifyGreen = Color(red: 0.11, green: 0.72, blue: 0.33) // Hex #1DB954
    static let spotifyGreen = Color(hex: "#E4F9EC")
//    static let netflixRed = Color(hex: "#E509131F")
    static let netflixRed = Color(red: 0.89, green: 0.11, blue: 0.14, opacity: 0.12) // Hex #E31313 with 12% opacity
    static let customBlack = Color(hex: "#1C1B1F")
    static let interactiveGray = Color(hex: "#767677")
    static let notifyRed = Color(hex: "#D50404")
    static let playstationBlue = Color(hex: "#0160B9").opacity(0.12)
    static let messageBubble = Color(hex: "#7211AF")
    static let divider = Color(hex: "#E7E7E7")
    static let textPrimary = Color(hex: "#1B1A1C")
}

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0) // Default to black
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
