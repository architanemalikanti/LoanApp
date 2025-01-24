//
//  BankerView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/23/25.
//

import SwiftUI

struct BankerView: View {
    var body: some View {
        VStack {
            HeaderView(
                title: "Today's Loan Applicants",
                subtitle: "",
                angle: -10,
                background: .purple
            )
            .offset(y: 50)
        }
        
    }
}
