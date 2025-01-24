//
//  TLButton.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/16/25.
//

import Foundation
import SwiftUI


struct TLButton: View {
    
    let title: String
    let background: Color
    let action: () -> Void
    
    var body: some View {
        Button {
            //action
            action()
            
        } label: {
            ZStack {
                RoundedRectangle(cornerRadius: 10)
                    .foregroundColor(background)
                
                Text(title)
                    .foregroundColor(Color.white)
                    .bold()
            }
        }
    }
    
}
