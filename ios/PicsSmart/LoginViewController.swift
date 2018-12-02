//
//  LoginViewController.swift
//  PicsSmart
//
//  Created by Yaroslav Spirin on 12/2/18.
//  Copyright © 2018 Mountain Viewer. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {

    @IBOutlet weak var loginButton: UIButton!
    
    @IBAction func loginButtonTouchUpInside(_ sender: Any) {
        performSegue(withIdentifier: "InstagramAuthSegue", sender: self)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
}
