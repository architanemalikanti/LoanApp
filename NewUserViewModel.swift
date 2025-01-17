//
//  NewUserViewModel.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/16/25.

import Foundation

class NewUserViewModel: ObservableObject {
    @Published var title = ""
    @Published var showAlert = false
    
    init() {}
    
    func save() {
        
    }
    
    
    var canSave: Bool {
        guard !title.trimmingCharacters(in: .whitespaces).isEmpty else {
            return false
        }
        return true
    }
    
}


