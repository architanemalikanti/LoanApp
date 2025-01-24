//
//  MainViewViewModel.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/23/25.
//

import Foundation

class MainViewViewModel: ObservableObject {
    @Published var currentUserId: Int = 0 // Ensure this matches the backend type
    @Published var isSignedIn: Bool = false
    @Published var userRole: String = "" // "banker" or "user"
    
    func fetchAuthStatus() {
        print("fetchAuthStatus called")
        guard let url = URL(string: "http://127.0.0.1:8000//auth/status") else {
            print("Invalid URL")
            return
        }

        guard let sessionToken = UserDefaults.standard.string(forKey: "session_token") else {
            print("No session token found")
            return
        }
        print("Session token found: \(sessionToken)")

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.addValue("Bearer \(sessionToken)", forHTTPHeaderField: "Authorization")

        let task = URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            guard let self = self, let data = data, error == nil else {
                print("Error fetching auth status: \(error?.localizedDescription ?? "Unknown error")")
                return
            }

            // Debugging raw response
            let responseString = String(data: data, encoding: .utf8)
            print("Raw response string: \(responseString ?? "Invalid data")")

            // Ensure JSON parsing is robust
            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as? [String: Any] {
                    DispatchQueue.main.async {
                        print("Backend response: \(json)")
                        self.isSignedIn = json["isSignedIn"] as? Bool ?? false
                        self.currentUserId = json["userId"] as? Int ?? 0
                        self.userRole = json["role"] as? String ?? ""
                        print("Parsed values - isSignedIn: \(self.isSignedIn), userId: \(self.currentUserId), role: \(self.userRole)")
                    }
                } else {
                    print("Failed to cast JSON as dictionary")
                }
            } catch {
                print("Failed to parse JSON: \(error)")
            }
        }

        task.resume()
    }

}
