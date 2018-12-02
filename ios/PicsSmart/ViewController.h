//
//  ViewController.h
//  picsart.ai-hack
//
//  Created by Vladislav Shakhray on 01/12/2018.
//  Copyright © 2018 Vladislav Shakhray. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ResultTableViewCell.h"

@interface ViewController : UIViewController <UITableViewDelegate, UITableViewDataSource, UIScrollViewDelegate>
@property (weak, nonatomic) IBOutlet UIButton *shareImage;
@property (weak, nonatomic) IBOutlet UIImageView *mainImageView;
@property (weak, nonatomic) IBOutlet UITableView *tableView;
@property (weak, nonatomic) UIView* view;
@property (weak, nonatomic) IBOutlet UIButton *backButton;
@property CAGradientLayer *gradient;
@property NSArray* probabilities;
@property NSArray* photos;
@property NSArray* names;
@property NSArray* nicks;
@property UIImage* mainImage;
// Positioning
@property CGFloat tableBottomOffset;
@property CGFloat tableTopOffset;
@property CGFloat savedTableViewOffset;
@property CGFloat offsetDiff;
@property (retain, nonatomic) NSArray *results;
@end

