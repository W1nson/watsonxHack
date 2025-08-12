//
//  FontExtensions.swift
//  iOS
//
//  Created by Jessica Trans on 8/9/25.
//

import SwiftUI

extension Font {
    static func setCustom(fontStyle: Font.TextStyle = .body, fontWeight: Weight = .regular) -> Font {
        return Font.custom(CustomFont(weight: fontWeight).rawValue, size: fontStyle.size)
    }
}

extension Font.TextStyle {
    var size: CGFloat {
        switch self {
            case .largeTitle: return 28
            case .title: return 16
            case .title2: return 14
            case .title3: return 12
            case .headline: return 20
            case .body: return 14
            case .callout: return 16
            case .subheadline: return 15
            case .footnote: return 13
            case .caption: return 12
            case .caption2: return 11
        @unknown default:
            return 8
        }
    }
}

enum CustomFont: String {
    case regular = "Geist-Regular"
    case semibold = "Geist-SemiBold"
    case medium = "Geist-Medium"
    case bold = "Geist-Bold"
    
    init(weight: Font.Weight) {
        switch weight {
            case .regular:
                self = .regular
            case .semibold:
                self = .semibold
            case .medium:
                self = .medium
            case .bold:
                self = .bold
            default:
                self = .regular
            }
    }
}
