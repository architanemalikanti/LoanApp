import Foundation
import SwiftUI

struct LoginView: View {
    
    @State var email = ""
    @State var selectedNumberOfPeople = 1 // Default selection for the picker

    var body: some View {
        
        NavigationView {
            VStack {
                // Header
                HeaderView(title: "Welcome to CascaAI👋 ",
                           subtitle: "Your AI Loan Assistant",
                           angle: 15,
                           background: .pink)
                
                // Form for selecting the number of people contesting for the loan
                Form {

                    Picker("Select Number of Loan Applicants", selection: $selectedNumberOfPeople) {
                        ForEach(1..<15, id: \.self) { number in
                            Text("\(number)").tag(number)
                        }
                    }
                    .pickerStyle(MenuPickerStyle()) // Dropdown-style picker
                    
                    // Use NavigationLink for navigation
                    NavigationLink(destination: InputUserInformationView()) {
                        ZStack {
                            RoundedRectangle(cornerRadius: 10)
                                .foregroundColor(Color.blue)
                            
                            Text("Next")
                                .foregroundColor(Color.white)
                                .bold()
                        }
                        .frame(height: 50)
                    }
                    
//                    Button {
//                        // what happens after you click "next"
//                        InputUserInformationView()
//                    } label: {
//                        ZStack {
//                            RoundedRectangle(cornerRadius: 10)
//                                .foregroundColor(Color.blue)
//                            
//                            Text("Next")
//                                .foregroundColor(Color.white)
//                                .bold()
//                        }
//                        .frame(height: 50)
//                    }
                }
                
                // learn about casca AI
                VStack {
                    Text("New around here?")
                    
                    
                    NavigationLink("Here's how we work.",
                                   destination: LearnMoreView())
                }
                .padding(.bottom, 50)
                Spacer()
            }

        }
        
        
        
        
    }
}
