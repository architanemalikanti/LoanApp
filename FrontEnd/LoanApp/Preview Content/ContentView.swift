//
//  ContentView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/15/25.
//

import SwiftUI

struct ContentView: View {
    @StateObject var viewModel = MainViewViewModel()
    
    var body: some View {
        NavigationView {
            if viewModel.isSignedIn {
                if viewModel.userRole == "banker" {
                    BankerView()
                } else if viewModel.userRole == "user" {
                    LoanApplicantView()
                }
            } else {
                LoginView()
            }
        }
        .onAppear {
            print("ContentView appeared") // Add this
            viewModel.fetchAuthStatus()
        }
    }
}

#Preview {
    ContentView()
}
