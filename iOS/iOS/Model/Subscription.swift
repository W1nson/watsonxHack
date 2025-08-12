//
//  UpcomingPayment.swift
//  iOS
//
//  Created by Jessica Trans on 8/11/25.
//

import Foundation
import SwiftUI

struct Subscription: Identifiable {
    let id = UUID().uuidString
    let name: String
    let amount: String
    let date: String
    let isFreeTrial: Bool
    let icon: Image
}

// mock data
let subscriptions = [
    Subscription(name: "Spotify - Premium",
            amount: "$11.99",
            date: "IN 2 DAYS",
            isFreeTrial: false,
            icon: Image("spotify")),
    Subscription(name: "Netflix - Standard",
            amount: "$17.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("netflix")),
    Subscription(name: "Google one - Premium",
            amount: "$9.99",
            date: "IN 3 DAYS",
            isFreeTrial: true,
            icon: Image("google_one")),
    Subscription(name: "PlayStation Plus",
            amount: "$99.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("playstation")),
    Subscription(name: "T-Mobile",
            amount: "$99.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("T-mobile")),
    Subscription(name: "Apple",
            amount: "$99.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("apple")),
    Subscription(name: "Pf",
            amount: "$99.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("pf")),
    Subscription(name: "iCloud",
            amount: "$99.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("icloud")),
    
    // repeat mock data
    Subscription(name: "Spotify - Premium",
            amount: "$11.99",
            date: "IN 2 DAYS",
            isFreeTrial: false,
            icon: Image("spotify")),
    Subscription(name: "Netflix - Standard",
            amount: "$17.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("netflix")),
    Subscription(name: "Google one - Premium",
            amount: "$9.99",
            date: "IN 3 DAYS",
            isFreeTrial: true,
            icon: Image("google_one")),
    Subscription(name: "PlayStation Plus",
            amount: "$99.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("playstation")),
    Subscription(name: "PlayStation Plus",
            amount: "$99.99",
            date: "IN 3 DAYS",
            isFreeTrial: false,
            icon: Image("playstation"))
]
