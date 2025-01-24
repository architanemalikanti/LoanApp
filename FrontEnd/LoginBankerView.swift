//
//  InputUserInformationView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/16/25.
//

import Foundation

import SwiftUI



struct LoginBankerView: View {
    @StateObject private var viewModel = BankerViewModel() // Correctly create a StateObject
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Header
                HeaderView(
                    title: "Banker Login",
                    subtitle: "Please fill out your details",
                    angle: -10,
                    background: .yellow
                )
                .offset(y: 50)
                
                // Login form
                Form {
                    // Show error message if any
                    if !viewModel.errorMessage.isEmpty {
                        Text(viewModel.errorMessage)
                            .foregroundColor(.red)
                    }
                    
                    TextField("Email Address", text: $viewModel.email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .autocapitalization(.none)
                        .keyboardType(.emailAddress)
                    
                    SecureField("Password", text: $viewModel.password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    Button(action: {
                        viewModel.login() // Call login on the viewModel
                    }) {
                        Text("Log In")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                }
            }
            .padding()
        }
    }
}
