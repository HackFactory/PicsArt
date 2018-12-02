//
//  InstagramAuthViewController.swift
//  PicsSmart
//
//  Created by Yaroslav Spirin on 12/2/18.
//  Copyright © 2018 Mountain Viewer. All rights reserved.
//

import UIKit
import SkyFloatingLabelTextField

class InstagramAuthViewController: UIViewController {
    
    var textField: SkyFloatingLabelTextField!
    
    @IBOutlet weak var continueButton: UIButton!
    
    @IBAction func continueButtonTouchUpInside(_ sender: Any) {
        performSegue(withIdentifier: "Picker", sender: self)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let vc = segue.destination as? PickerViewController {
            vc.username = textField!.text
        }
        
        
    }
    
    func setUpContinueButton() {
        continueButton.layer.cornerRadius = 10.0
    }
   
    func setUpInstagramUserName() {
        textField = SkyFloatingLabelTextField(frame: CGRect(x: 30, y: 272, width: 315, height: 45))
        textField.placeholder = "@username"
        textField.title = "Username"
        textField.lineColor = UIColor(red: 235.0 / 255.0, green: 90.0 / 255.0, blue: 90.0 / 255.0, alpha: 1.0)
        textField.addTarget(self, action: #selector(textFieldDidChange(_:)), for: .editingDidEndOnExit)
        self.view.addSubview(textField)
    }
    
    @objc func textFieldDidChange(_ textfield: UITextField) {
        textfield.resignFirstResponder()
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setUpInstagramUserName()
        setUpContinueButton()
    }

}
