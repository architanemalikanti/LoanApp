//
//  HeaderView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/15/25.
//

import Foundation

import SwiftUI

struct HeaderView: View {
    let title: String
    let subtitle: String
    let angle: Double
    let background: Color
    
    
    
    
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 0)
                .foregroundColor(background)
                .rotationEffect(Angle(degrees: angle))
                
            
            VStack {
                Text(title)
                    .font(.system(size: 20))
                    .foregroundColor(Color.white)
                    .bold()
                
                Text(subtitle)
                    .font(.system(size: 20))
                    .foregroundColor(Color.white)
            }
            .padding(.top, 30)
            
        }
        .frame(width: UIScreen.main.bounds.width * 3, height: 300)
        .offset(y: -190)
        Spacer()
    }
}

