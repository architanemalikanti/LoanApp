//
//  InputUserInformationView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/16/25.
//

import Foundation

import SwiftUI

struct LoginApplicantView: View {
    @StateObject var viewModel = LoanApplicantViewModel()
    @State var email = ""
    @State var password = ""
    
    var body: some View {
        NavigationView {
            
            VStack(spacing: 20) {
                // Header
                HeaderView(
                    title: "Loan Applicant Login",
                    subtitle: "Please fill out your details",
                    angle: -10,
                    background: .yellow
                    
                )
                .offset(y: 50)
                //login form
                Form {
                    TextField("Email Address", text: $email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    SecureField("Password", text: $email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    SBButton(
                        title: "Log In",
                        background: .green
                    ) {
                        //action:
                        //viewModel.register() // Call the register function
                    }
                }

                    
                }
                
            }
            
        }
        
    }

        
