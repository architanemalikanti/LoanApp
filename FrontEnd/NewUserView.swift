//
//  NewUserView.swift
//  LoanApp
//
//  Created by Archita Nemalikanti on 1/16/25.
//

import Foundation
import SwiftUI
import UniformTypeIdentifiers

struct NewUserView: View {
    @StateObject var viewModel = NewUserViewModel()
    @State private var showingDocumentPicker = false
    @State private var uploadedFileURL: URL?
    @Binding var newUserPresented: Bool
    
    var body: some View {
        VStack {
            // Title
            Text("New User")
                .font(.system(size: 32))
                .bold()
                .padding(.top, 100)
            
            Form {
                // User's name
                TextField("Full Name", text: $viewModel.title)
                
                // PDF upload section
                HStack {
                    Text("Bank Statement")
                        .font(.headline)
                    
                    Spacer()
                    
                    Button(action: {
                        showingDocumentPicker = true
                    }) {
                        Text("Upload PDF")
                            .foregroundColor(.blue)
                    }
                }
                
                // Display uploaded PDF name
                if let fileName = uploadedFileURL?.lastPathComponent {
                    Text("Uploaded: \(fileName)")
                        .foregroundColor(.green)
                }
                
                // Save button
                TLButton(title: "Save",
                         background: .pink) {
                    
                    if viewModel.canSave {
                        viewModel.save()
                        newUserPresented = false
                    } else {
                        viewModel.showAlert = true
                    }
                    
                }
                .padding()
            }
            .alert(isPresented: $viewModel.showAlert) {
                
                Alert(title: Text("Error"), message: Text("Please fill in all fields."))
                
            }
                
            
        }
        .sheet(isPresented: $showingDocumentPicker) {
            DocumentPicker(uploadedFileURL: $uploadedFileURL)
        }
    }
}

// Custom DocumentPicker
struct DocumentPicker: UIViewControllerRepresentable {
    @Binding var uploadedFileURL: URL?

    func makeCoordinator() -> Coordinator {
        return Coordinator(self)
    }

    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [UTType.pdf])
        picker.allowsMultipleSelection = false
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}

    class Coordinator: NSObject, UIDocumentPickerDelegate {
        let parent: DocumentPicker

        init(_ parent: DocumentPicker) {
            self.parent = parent
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            parent.uploadedFileURL = urls.first
        }

        func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
            print("Document picker cancelled.")
        }
    }
}

