//
//  PickerViewController.swift
//  PicsSmart
//
//  Created by Yaroslav Spirin on 12/2/18.
//  Copyright © 2018 Mountain Viewer. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON
import SDWebImage
import SVProgressHUD

@objc public class CellInfo: NSObject {
    var image: UIImage
    var userName: String
    var fullName: String
    var proba: Double
    
    init(_ image: UIImage, _ userName: String, _ fullName: String, _ proba: Double) {
        self.image = image
        self.userName = userName
        self.fullName = fullName
        self.proba = proba
    }
}

class PickerViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    @IBOutlet weak var containerView: UIView!
    
    @IBOutlet weak var detailButton: UIButton!
    
    var results = [Any]()
    let imagePicker = UIImagePickerController()
    var username: String? = nil
    
    @IBOutlet weak var pickedImage: UIImageView!
    
    @IBOutlet weak var pickPhotoButton: UIButton!
    
    var bufferImage: UIImage? {
        didSet {
            pickedImage.image = bufferImage
            sendPickedImage()
            SVProgressHUD.show()
        }
    }

    func resizeImage(image: UIImage, newWidth: CGFloat) -> UIImage? {
        
        let scale = newWidth / image.size.width
        let newHeight = image.size.height * scale
        UIGraphicsBeginImageContext(CGSize(width: newWidth, height: newHeight))
        image.draw(in: CGRect(x: 0, y: 0, width: newWidth, height: newHeight))
        let newImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        
        return newImage
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let vc = segue.destination as? ViewController {
            vc.mainImage = pickedImage.image
            vc.results = results
        }
    }
    
    @IBAction func detailButtonTouchUpInside(_ sender: Any) {
        performSegue(withIdentifier: "DetailSegue", sender: self)
    }
    
    @IBAction func pickPhotoButtonTouchUpInside(_ sender: Any) {
        present(imagePicker, animated: true, completion: nil)
    }
    
    func setUpPickPhotoButton() {
        pickPhotoButton.layer.cornerRadius = 10.0
    }
    
    func setUpPickedImage() {
        pickedImage.layer.cornerRadius = 20.0
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        
        if let image = info[.originalImage] as? UIImage {
            bufferImage = image
        }
        
        dismiss(animated: true, completion: nil)
    }
    
    func requestWith(endUrl: String,
                     imageData: Data?,
                     parameters: [String : Any],
                     onCompletion: (([String: Any]?) -> Void)? = nil,
                     onError: ((Error?) -> Void)? = nil) {
        
        let url = endUrl
        
        let headers: HTTPHeaders = [
            /* "Authorization": "your_access_token",  in case you need authorization header */
            "Content-type": "multipart/form-data"
        ]
        
        Alamofire.upload(multipartFormData: { (multipartFormData) in
            for (key, value) in parameters {
                multipartFormData.append("\(value)".data(using: String.Encoding.utf8)!, withName: key as String)
            }
            
            if let data = imageData{
                multipartFormData.append(data, withName: "image", fileName: "image.jpg", mimeType: "image/jpeg")
            }
            
        }, usingThreshold: UInt64.init(), to: url, method: .post, headers: headers) { (result) in
            switch result {
            case .success(let upload, _, _):
                upload.responseJSON { response in
                    print("Successfully uploaded")
                    
                    if let data = response.data {
                        let json = JSON(data)
                        self.results = [Any]()
                        
                        if let array = json.array {
                            for elem in array {
                                if let description = elem.array {
                                    let image = description[0].stringValue
                                    let userName = description[1].stringValue
                                    let fullName = description[2].stringValue
                                    let proba = description[3].doubleValue
                                    
                                    let imageView = UIImageView(frame: CGRect(x: 0, y: 0, width: 10, height: 10))
                            
                                        imageView.sd_setImage(with: URL(string: image), completed: { (_, _, _, _) in
                                            let cellInfo = CellInfo(imageView.image!,
                                                                    userName,
                                                                    fullName,
                                                                    proba)
                                            
                                            var dict = NSMutableDictionary()
                                            dict["image"] = imageView.image!
                                            dict["userName"] = userName
                                            dict["fullName"] = fullName
                                            dict["proba"] = proba
                                            self.results.append(dict)
                                            self.detailButton.isHidden = false
                                            SVProgressHUD.dismiss()
                                        })
                                }
                            }
                        }
                        
                        print("hello")
                    } else {
                        return
                    }
                    
                    //let json = JSON(response.data)
                    if let err = response.error {
                        onError?(err)
                        return
                    }
                    
                    onCompletion?(nil)
                }
            case .failure(let error):
                print("Error in upload: \(error.localizedDescription)")
                onError?(error)
            }
        }
    }
    
    func sendUsername() {
        let urlString = "http://35.173.129.19:8888/instagram_preprocessing/"
        
        guard let userName = username else {
            return
        }
        
        Alamofire.request(urlString,
                          method: .get,
                          parameters: ["login": userName],
                          encoding: URLEncoding.queryString,
                          headers: nil).responseJSON {
            response in
            switch response.result {
            case .success:
                print(response)
                break
            case .failure(let error):
                
                print(error)
            }
        }
    }
    
    func sendPickedImage() {
        requestWith(endUrl: "http://35.173.129.19:8888/analyze_galery/",
                    imageData: pickedImage.image?.jpegData(compressionQuality: 0.3),
                    parameters: [:])
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        dismiss(animated: true, completion:nil)
    }
    
    func setUpContainerView() {
        containerView.layer.cornerRadius = 20.0
        containerView.layer.shadowOffset = CGSize(width: 2.0, height: 2.0)
        containerView.layer.shadowOpacity = 1.0
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setUpPickPhotoButton()
        setUpPickedImage()
        sendUsername()
        setUpContainerView()
        
        detailButton.isHidden = true
        imagePicker.delegate = self
        imagePicker.allowsEditing = false
        imagePicker.sourceType = .photoLibrary
    }

}
