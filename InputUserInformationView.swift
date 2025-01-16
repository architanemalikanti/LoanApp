//
//  InputUserInformationView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/16/25.
//

import Foundation

import SwiftUI

struct InputUserInformationView: View {
    
    var body: some View {
        VStack(spacing: 20) {
            // Header
            HeaderView(
                title: "User Information",
                subtitle: "Please fill out your details",
                angle: -10,
                background: .blue
            )
            .offset(y: 50)
            
        }
    }
}
        
