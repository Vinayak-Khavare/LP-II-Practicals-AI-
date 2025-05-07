1. Contact-Opportunity Mapper

```
public class ContactOpportunityMapper {
    public static Map<Id, List<Opportunity>> mapContactsToOpportunities(List<Contact> contacts) {
        Set<Id> accountIds = new Set<Id>();
        for (Contact c : contacts) {
            if (c.AccountId != null) {
                accountIds.add(c.AccountId);
            }
        }

        Map<Id, List<Opportunity>> accountToOpps = new Map<Id, List<Opportunity>>();
        for (Opportunity opp : [SELECT Id, Name, AccountId FROM Opportunity WHERE AccountId IN :accountIds]) {
            if (!accountToOpps.containsKey(opp.AccountId)) {
                accountToOpps.put(opp.AccountId, new List<Opportunity>());
            }
            accountToOpps.get(opp.AccountId).add(opp);
        }

        Map<Id, List<Opportunity>> contactToOpportunities = new Map<Id, List<Opportunity>>();
        for (Contact c : contacts) {
            List<Opportunity> relatedOpps = accountToOpps.get(c.AccountId);
            contactToOpportunities.put(c.Id, relatedOpps != null ? relatedOpps : new List<Opportunity>());
        }

        return contactToOpportunities;
    }
}
```

---

2. Calculate Stage_Progress\_\_c on Account

```
public class AccountStageProgressCalculator {
    public static void updateAccountStageProgress(List<Account> accounts) {
        Set<Id> accountIds = new Set<Id>();
        for (Account acc : accounts) {
            accountIds.add(acc.Id);
        }

        Map<String, Integer> stageWeightMap = new Map<String, Integer>{
            'Prospecting' => 25,
            'Qualification' => 35,
            'Proposal' => 45,
            'Negotiation' => 50,
            'Closed Won' => 100
        };

        Map<Id, List<Opportunity>> accountOppsMap = new Map<Id, List<Opportunity>>();
        for (Opportunity opp : [
            SELECT Id, StageName, AccountId
            FROM Opportunity
            WHERE AccountId IN :accountIds
        ]) {
            if (!accountOppsMap.containsKey(opp.AccountId)) {
                accountOppsMap.put(opp.AccountId, new List<Opportunity>());
            }
            accountOppsMap.get(opp.AccountId).add(opp);
        }

        List<Account> accountsToUpdate = new List<Account>();
        for (Account acc : accounts) {
            List<Opportunity> opps = accountOppsMap.get(acc.Id);
            if (opps != null && !opps.isEmpty()) {
                Integer total = 0;
                for (Opportunity opp : opps) {
                    total += stageWeightMap.containsKey(opp.StageName) ? stageWeightMap.get(opp.StageName) : 0;
                }
                Decimal avg = total / opps.size();
                acc.Stage_Progress__c = avg;
                accountsToUpdate.add(acc);
            }
        }

        update accountsToUpdate;
    }
}
```

---

3. Generate Opportunity Report (Probability > 50%)

```
public class OpportunityReportGenerator {
    public static String generateHighProbabilityReport() {
        List<Opportunity> opps = [
            SELECT Name, Probability, CloseDate, Amount
            FROM Opportunity
            WHERE Probability > 50
            ORDER BY CloseDate ASC
        ];

        String report = 'Opportunity Report (Probability > 50%)\n';
        report += '---------------------------------------\n';
        report += 'Name | Probability | Close Date | Amount\n';

        for (Opportunity opp : opps) {
            report += opp.Name + ' | ' + opp.Probability + '% | ' + opp.CloseDate.format() + ' | $' + opp.Amount + '\n';
        }

        return report;
    }
}
```

---

4. Simple Calculator

```
public class Calculator {
    public static Decimal calculate(Decimal num1, Decimal num2, String operator) {
        if (operator == '+') return num1 + num2;
        else if (operator == '-') return num1 - num2;
        else if (operator == '*') return num1 * num2;
        else if (operator == '/') {
            if (num2 == 0) throw new ArithmeticException('Division by zero');
            return num1 / num2;
        }
        else throw new IllegalArgumentException('Invalid operator: ' + operator);
    }
}
```

---
