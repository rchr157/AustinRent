# AustinRent
This project examines the cost of rent in Austin. The purpose of this project is to get a general understanding of what influences the cost of rent for an apartment in Austin and how it differs by number of bedrooms, squarefoot, and location. This is for preperation for moving to Austin.
![Image of Apartments Clustered](https://github.com/rchr157/AustinRent/blob/master/screenshots/snap3-austin-rent-clustered.png)

# Objective
The objectives of this project included:
- Determine Average Rent of 1-bedroom apartment in Austin
- Understand what type of apartments are available in Austin
- Understand relationship between rent and features
- Determine Square foot distribution of apartments in Austin
- Get an estimate of a 1-bedroom apartment in specific location.

## Features considered
The features that were observed from the data set included:
- Date
- Number of Beds
- Number of Bathrooms
- Size of apartment (Square foot)
- Location

## Assumptions
Initial Assumptions for this project included:
- Number of Beds would be a major influence on the price of rent (more bedrooms == higher rent)
- Location would also be a majore influence on price of rent (some areas are more expensive/cheaper than others)

## Observations:
The initial assumption of having more bedrooms means having higher rent was not as accurate as I had initially thought. When looking at the relationship between bedrooms and rent, the data showed a weak linear relationship, the average rent slightly varied over the number of bedrooms in the apartment. At closer examination, it is actaully the square foot of the apartment that has more of an influence on rent. When looking at the distribution of square foot by number of bedrooms, one can notice that bedrooms can vary largely in square foot, e.g. there are studios that are as big as 2-bedroom apartments. This large variance of size for each bedroom apartment weakens the relationship between number of bedrooms and price of rent. In turn, square foot has a stronger correlation to cost of rent.
![Image of Squarefoot distribution by bedrooms](https://github.com/rchr157/AustinRent/blob/master/screenshots/snap6-sqft-bed-catplot.png)

When viewing the boxplot for number of bedrooms and squarfoot, there were several datapoints that fell outside the IQR whiskers.  Examining the data points, the initial hypothesis was that it had to do with its location. Based on the addresses included in the dataset, the latitude and logitude was determined with geopy.The datapoints were plotted on a map with the marker size representing the square foot of the apartment, and the color representing the cost of rent. The outliers that were seen earlier are all located in the same area.
![Image of Austin Map](https://github.com/rchr157/AustinRent/blob/master/screenshots/snap1-austin-rent-overview.png)
