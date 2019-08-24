# finpy
finpy is a booking tool written in python

## features
- monthly/daily incomes/outcomes with start date and end date
- calculate income/outcome/balance in a day
- calculate average/detailed/sum of income/outcome/balance over a time range
- macros

## adding income/outcome
```>> add_income#{MON,DAY}, <description>, <value (> 0)>, <start date>, <end date>```  
```>> add_outcome#{MON,DAY}, <description>, <value (< 0)>, <start date>, <end date>```
- {MON,DAY}: Monthly or daily income (monthly incomes are only used for calculations in the first day of the month)

## calculations by day
```>> calculate_income#<date>```  
```>> calculate_outcome#<date>```  
```>> calculate_balance#<date>```

## calculations by range
SYNTAX: ```<daytype-function>·<varied argument index>→<{d: date/i: int}><value to loop towards>[|<output-function>, default=sum_range]```

output-function: print_range | avg_range | sum_range

Example: ```calculate_income#2019-09-01·0→d2019-10-01```  
Calculates income from Sept 2019 to Oct 2019 then adds the values

## example
```
>> AI~add_income
AI now points to add_income # Macro system
>> AO~add_outcome
AO now points to add_outcome
>> AI#MON,Salary,5200,2019-05-01,2025-05-01
AI#MON,Salary,5200,2019-05-01,2025-05-01: Salary: 5200/MON 2019-05-01 to 2025-05-01 (<class 'models.Income'>)
>> AO#DAY,Food,7.5,2019-05-01,2025-05-01
Outcomes must have negative value
>> AO#DAY,Food,-7.5,2019-05-01,2025-05-01
AO#DAY,Food,-7.5,2019-05-01,2025-05-01: Food: -7.5/DAY 2019-05-01 to 2025-05-01 (<class 'models.Outcome'>)
>> CB~calculate_balance
CB now points to calculate_balance
>> CB#2019-08-01
CB#2019-08-01: 5192.5 (<class 'decimal.Decimal'>)
>> CB#2019-08-05
CB#2019-08-05: -7.5 (<class 'decimal.Decimal'>)
>> CB#2019-08-01·0→d2019-12-24
24912.5
```