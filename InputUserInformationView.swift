//
//  InputUserInformationView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/16/25.
//

import Foundation

import SwiftUI

struct InputUserInformationView: View {
    @StateObject var viewModel = InputUserInformationViewModel()
    
    var body: some View {
        NavigationView {
            
            VStack(spacing: 20) {
                // Header
                HeaderView(
                    title: "User Information",
                    subtitle: "Please fill out your details",
                    angle: -10,
                    background: .yellow
                    
                )
                .offset(y: 50)
                
                .toolbar {
                    Button {
                        //action
                        viewModel.showingNewUserView = true
                        
                    } label: {
                        Image(systemName: "plus")
                    }
                }
                .sheet(isPresented: $viewModel.showingNewUserView){
                    NewUserView()
                    
                }
                
            }
            
        }
        
    }
}
        
