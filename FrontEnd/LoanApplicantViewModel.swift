//
//  BankerViewModel.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/21/25.
//

import Foundation

class LoanApplicantViewModel: ObservableObject {
    
    @Published var email = ""
    @Published var password = ""
    @Published var errorMessage = ""
    
    var mainViewViewModel: MainViewViewModel? // Add a reference to MainViewViewModel
    
    init(mainViewViewModel: MainViewViewModel? = nil) {
        self.mainViewViewModel = mainViewViewModel
    }
        
         func login() {
            
            //first, validate the user
            guard validate() else {
                return
            }
            
            // Create the URL for the backend endpoint
            guard let url = URL(string: "http://127.0.0.1:8000/bankUser/") else {
                errorMessage = "Invalid URL."
                return
            }
            
            // Prepare the request body
            let requestBody: [String: Any] = [
                "email": email,
                "password": password
            ]
            
            do {
                let jsonData = try JSONSerialization.data(withJSONObject: requestBody, options: [])
                
                // Configure the URLRequest
                var request = URLRequest(url: url)
                request.httpMethod = "POST"
                request.setValue("application/json", forHTTPHeaderField: "Content-Type")
                request.httpBody = jsonData
                
                // Send the request
                URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
                    DispatchQueue.main.async {
                        if let error = error {
                            self?.errorMessage = "Error: \(error.localizedDescription)"
                            return
                        }
                        
                        guard let data = data else {
                            self?.errorMessage = "No response data."
                            return
                        }
                        
                        do {
                            // Parse the response
                            if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                                if let success = json["success"] as? Bool, success {
                                    // Successfully logged in
                                    if let sessionToken = json["session_token"] as? String {
                                        UserDefaults.standard.set(sessionToken, forKey: "session_token")
                                        self?.errorMessage = "Login successful!"
                                        
                                        // Call fetchAuthStatus after login
                                        self?.mainViewViewModel?.fetchAuthStatus()
                                    }
                                } else {
                                    self?.errorMessage = json["error"] as? String ?? "Unknown error occurred."
                                }
                            }
                        } catch {
                            self?.errorMessage = "Failed to parse response."
                        }
                    }
                }.resume()
            } catch {
                errorMessage = "Failed to encode request body."
            }
        }
        
        
        func validate() -> Bool {
            let trimmedEmail = email.trimmingCharacters(in: .whitespaces)
            
            errorMessage = ""
            guard !email.trimmingCharacters(in: .whitespaces).isEmpty,
                  !password.trimmingCharacters(in: .whitespaces).isEmpty else {
                
                errorMessage = "Please fill in all fields."
                return false
            }
            
            return true
            
            
        }
    
}
