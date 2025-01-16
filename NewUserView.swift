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
    
    var body: some View {
        VStack {
            
            //title:
            Text("New User")
                .font(.system(size: 32))
                .bold()
            
            
            Form {
                //getting the name of user
                TextField("Full Name", text: $viewModel.title)
                
                // Getting the PDF of bank statement
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
                
                // Button
                TLButton(title: "Save",
                         background: .pink) {
                    viewModel.save()
                }
                         .padding()
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
