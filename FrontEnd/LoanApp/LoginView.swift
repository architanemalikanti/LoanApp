import Foundation
import SwiftUI

struct LoginView: View {
    
    @State var email = ""

    var body: some View {
        
        NavigationView {
            VStack {
                // Header
                HeaderView(title: "Welcome to CascaAI 👋 ",
                           subtitle: "Your AI Loan Assistant",
                           angle: 15,
                           background: .pink)
                
                // Form for selecting the number of people contesting for the loan
                Form {

                    
                    // Use NavigationLink for navigation
                    NavigationLink(destination: LoginBankerView()) {
                        ZStack {
                            RoundedRectangle(cornerRadius: 10)
                                .foregroundColor(Color.blue)
                            
                            Text("Login As a Banker🏦")
                                .foregroundColor(Color.white)
                                .bold()
                        }
                        .frame(height: 50)
                    }
                    // Use NavigationLink for navigation
                    NavigationLink(destination: LoginApplicantView()) {
                        ZStack {
                            RoundedRectangle(cornerRadius: 10)
                                .foregroundColor(Color.blue)
                            
                            Text("Login As a Loan Applicant👨‍💼")
                                .foregroundColor(Color.white)
                                .bold()
                        }
                        .frame(height: 50)
                    }
                    
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
