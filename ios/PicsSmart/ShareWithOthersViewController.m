//
//  ShareWithOthersViewController.m
//  picsart.ai-hack
//
//  Created by Vladislav Shakhray on 02/12/2018.
//  Copyright © 2018 Vladislav Shakhray. All rights reserved.
//

#import "ShareWithOthersViewController.h"

@interface ShareWithOthersViewController ()

@end

@implementation ShareWithOthersViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}
- (IBAction)close:(id)sender {
}

-(IBAction)prepareForUnwind:(UIStoryboardSegue *)segue {
}
- (void) viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    CGFloat fl = 20;
    _instagram.layer.cornerRadius = fl;
    _facebook.layer.cornerRadius = fl;
    _snapchat.layer.cornerRadius = fl;
    _picsart.layer.cornerRadius = fl;
    _instagram.clipsToBounds = true;
    _facebook.clipsToBounds = true;
    _snapchat.clipsToBounds = true;
    _picsart.clipsToBounds = true;
}
- (IBAction)shareInstagram:(id)sender {
     [[UIApplication sharedApplication] openURL:[NSURL URLWithString: @"https://www.instagram.com"]];
}
- (IBAction)shareFacebook:(id)sender {
     [[UIApplication sharedApplication] openURL:[NSURL URLWithString: @"https://www.facebook.com"]];
}
- (IBAction)snapchat:(id)sender {
     [[UIApplication sharedApplication] openURL:[NSURL URLWithString: @"https://www.snapchat.com"]];
}
- (IBAction)picsArt:(id)sender {
     [[UIApplication sharedApplication] openURL:[NSURL URLWithString: @"https://picsart.com"]];
}
/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
