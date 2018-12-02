//
//  ViewController.m
//  picsart.ai-hack
//
//  Created by Vladislav Shakhray on 01/12/2018.
//  Copyright © 2018 Vladislav Shakhray. All rights reserved.
//

#import "ViewController.h"
#import "PicsSmart-Swift.h"

const float cr = 14;
const float max99 = .8;
@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    _tableView.delegate = self;
    _tableView.dataSource = self;
    _tableView.allowsSelection = false;
    NSMutableArray* a1, *a2, *a3, *a4;
    a1 = [NSMutableArray new];
    a2 = [NSMutableArray new];
    a3 = [NSMutableArray new];
    a4 = [NSMutableArray new];
    NSLog(@"%@", _results);
    NSLog(@"%@", _results[0]);
    for (NSDictionary* dict in _results) {
        NSString* name = dict[@"fullName"];
        NSString* userName = dict[@"userName"];
        UIImage* image = dict[@"image"];
        NSString* proba = dict[@"proba"];
        [a1 addObject:image];
        [a2 addObject:name];
        [a3 addObject:userName];
        [a4 addObject:proba];
    }
    _photos = [NSArray arrayWithArray:a1];
    _names = [NSArray arrayWithArray:a2];
    _nicks = [NSArray arrayWithArray:a3];
    _probabilities = [NSArray arrayWithArray:a4];
    //_mainImage = [UIImage imageNamed:@"model"];
    _mainImageView.image = _mainImage;
//    _view = [[UIView alloc]initWithFrame:_tableView.frame];

}
- (IBAction)goBack:(id)sender {
    [self performSegueWithIdentifier:@"BackSegue" sender:self];
}
-(IBAction)prepareForUnwind:(UIStoryboardSegue *)segue {
}
- (void) viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
//    _header.frame = CGRectMake(0, _tableView.frame.origin.y-cr, self.view.frame.size.width, cr);
//    _header.backgroundColor = [UIColor colorWithRed:245.4/255 green:245.4/255 blue:245.4/255 alpha:1];
//    _header.clipsToBounds = true;
//    _header.layer.masksToBounds = true;
//    _header.layer.cornerRadius = cr;
//    _tableView.layer.shadowColor = [UIColor colorWithWhite:0.1 alpha:1].CGColor;
//    _tableView.layer.shadowRadius = 300;
//    _tableView.layer.shadowOffset = CGSizeMake(0, 0);
//    _tableView.layer.shadowOpacity = 1.;
//    _tableView.clipsToBounds = false;
    _shareImage.layer.cornerRadius = _shareImage.frame.size.width / 2;
    _shareImage.clipsToBounds = true;
    _offsetDiff = _mainImageView.frame.size.height - _shareImage.frame.origin.y;
//    NSLog(@"%f", _offsetDiff);
}
- (void) viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];
    _tableBottomOffset = _tableView.frame.origin.y;
    _tableTopOffset = 180;
    _tableView.superview.layer.cornerRadius = cr;
    _tableView.superview.layer.masksToBounds = true;
    _gradient = [CAGradientLayer layer];
    _gradient.frame = CGRectMake(0, 0, self.view.frame.size.width, _tableBottomOffset + 110);
    _gradient.colors = @[(id)[UIColor colorWithWhite:1 alpha:0].CGColor, (id)[UIColor colorWithWhite:0 alpha:0.6].CGColor];
    
    [_mainImageView.layer insertSublayer:_gradient atIndex:0];

}

- (void) openShareMenu: (UIButton*) sender {
    NSLog(@"pressed!");
}

- (nonnull UITableViewCell *)tableView:(nonnull UITableView *)tableView cellForRowAtIndexPath:(nonnull NSIndexPath *)indexPath {
    ResultTableViewCell* cell = [tableView dequeueReusableCellWithIdentifier:@"result" forIndexPath:indexPath];
    cell.photo.image = _photos[indexPath.row];
    cell.photo.layer.cornerRadius = cell.photo.frame.size.height / 2.;
    cell.photo.layer.masksToBounds = true;
    float val = [(NSNumber*)(_probabilities[indexPath.row]) floatValue] * 100;
    cell.rating.text = [NSString stringWithFormat:@"%.01f%%", val];
    cell.rating.layer.cornerRadius = cell.rating.frame.size.height / 2;
    cell.rating.layer.borderColor = [UIColor colorWithRed:227./255 green:74./255 blue:55./255 alpha:1].CGColor;
    cell.rating.layer.borderWidth = 2;
    cell.name.text = _names[indexPath.row];
    cell.nickname.text = _nicks[indexPath.row];
    if (val < max99 * 100) {
        cell.approved.hidden = true;
    } else {
        cell.approved.hidden = false;
    }
    return cell;
}

- (NSInteger)tableView:(nonnull UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return _names.count;
}

- (CGFloat) tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
    CGFloat rowHeight = 82;
//    if (indexPath.row == 0) {
//        return rowHeight + 15;
//    }
    return rowHeight;
}

- (void)scrollViewWillBeginDragging:(UIScrollView *)scrollView {
    _savedTableViewOffset = scrollView.contentOffset.y;
}

- (void)scrollViewDidScroll:(UIScrollView *)scrollView {
    CGFloat offset = _tableView.frame.origin.y;
    CGFloat contentOffset = _tableView.contentOffset.y;
    static CGFloat previousOffset;
    bool shouldStop = false;
    if (offset <= _tableTopOffset && contentOffset >= 0) {
        offset = _tableTopOffset;
        shouldStop = true;
    }
    if (offset >= _tableBottomOffset && contentOffset <= 0) {
        offset = _tableBottomOffset;
        shouldStop = true;
    }
    if (shouldStop) {
        CGRect frame = scrollView.frame;
        frame.origin.y = offset;
        frame.size.height = self.view.frame.size.height - frame.origin.y;
        scrollView.frame = frame;
//        _header.frame = CGRectMake(0, _tableView.frame.origin.y-cr, self.view.frame.size.width, 2 * cr);
        frame = _mainImageView.frame;
        if (offset >= _tableBottomOffset && contentOffset <= 0)
        frame.size.height = scrollView.frame.origin.y - contentOffset - frame.origin.y;
        else
            frame.size.height = scrollView.frame.origin.y - frame.origin.y;
        _mainImageView.frame = frame;
        frame = _shareImage.frame;
        frame.origin.y = _mainImageView.frame.size.height - _offsetDiff;
        _shareImage.frame = frame;
//        _gradient.frame = _mainImageView.frame;
        _savedTableViewOffset = 0;
        return;
    }
    
//    NSLog(@"BEFORE: %f\t\t%f", offset, scrollView.contentOffset.y);
    CGRect rect = scrollView.frame;
    rect.origin.y += previousOffset - scrollView.contentOffset.y;
    previousOffset = scrollView.contentOffset.y;
    [scrollView setContentOffset:CGPointMake(scrollView.contentOffset.x, _savedTableViewOffset)];
    rect.size.height = self.view.frame.size.height - rect.origin.y;
    scrollView.frame = rect;
//    _header.frame = CGRectMake(0, _tableView.frame.origin.y-cr, self.view.frame.size.width, 2 * cr);
    CGRect frame = _mainImageView.frame;
    frame.size.height = scrollView.frame.origin.y - frame.origin.y;
    _mainImageView.frame = frame;
    frame = _shareImage.frame;
    frame.origin.y = _mainImageView.frame.size.height - _offsetDiff;
    _shareImage.frame = frame;
//    _gradient.frame = _mainImageView.frame;
    _savedTableViewOffset = 0;
//    NSLog(@"AFTER: %f\t\t%f", offset, scrollView.contentOffset.y);
}

- (void) tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    [tableView deselectRowAtIndexPath:indexPath animated:NO];
}

//- (void) scrollViewDidScroll:(UIScrollView *)scrollView {
//    NSLog(@"%f", scrollView.contentOffset.y);
//    CGFloat offset = _tableView.frame.origin.y;
//    CGFloat contentOffset = _tableView.contentOffset.y;
//    if (offset >= _tableTopOffset && offset <= _tableBottomOffset) {
//        offset -= contentOffset;
//    }
//    if (offset < _tableTopOffset) {
//        offset = _tableTopOffset;
//    }
//    if (offset > _tableBottomOffset) {
//        offset = _tableBottomOffset;
//    }//    [_tableView setNeedsDisplay];
//}

@end
