//
//  ResultTableViewCell.h
//  picsart.ai-hack
//
//  Created by Vladislav Shakhray on 01/12/2018.
//  Copyright © 2018 Vladislav Shakhray. All rights reserved.
//

#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface ResultTableViewCell : UITableViewCell
@property (weak, nonatomic) IBOutlet UIImageView *photo;
@property (weak, nonatomic) IBOutlet UILabel *rating;
@property (weak, nonatomic) IBOutlet UILabel *name;
@property (weak, nonatomic) IBOutlet UILabel *nickname;
@property (weak, nonatomic) IBOutlet UIImageView *approved;

@end

NS_ASSUME_NONNULL_END
