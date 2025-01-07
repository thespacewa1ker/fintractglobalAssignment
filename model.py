class Bank:
    def __init__(self, id, name, country, street, city, postal_code, phone, email, legal_entity_identifier, bic):
        self.id = id
        self.name = name
        self.country = country
        self.address = {
            "street": street,
            "city": city,
            "postalCode": postal_code
        }
        self.contact = {
            "phone": phone,
            "email": email
        }
        self.legal_entity_identifier = legal_entity_identifier
        self.bic = bic

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "address": self.address,
            "contact": self.contact,
            "legalEntityIdentifier": self.legal_entity_identifier,
            "bic": self.bic
        }

class Branch:
    def __init__(self, id, name, bank_id, address, contact):
        self.id = id
        self.name = name
        self.bank_id = bank_id  # Reference to the associated bank
        self.address = address
        self.contact = contact

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bankId": self.bank_id,
            "address": self.address,
            "contact": self.contact
        }

class Customer_Bank_Account:
    def __init__(self, id, iban, account_type, bank_id, holder_name, address):
        self.id = id
        self.iban = iban
        self.account_type = account_type  # e.g., "savings", "checking"
        self.bank_id = bank_id  # Reference to the associated bank
        self.holder_name = holder_name  # Name of the account holder
        self.address = address  # Address information

    def to_dict(self):
        return {
            "id": self.id,
            "iban": self.iban,
            "accountType": self.account_type,
            "bankId": self.bank_id,
            "holderName": self.holder_name,
            "address": self.address  # Include address in output
        }

# account_model.py
class Business_Bank_Account:
    def __init__(self, id, iban, account_type, bank_id, holder_name, address):
        self.id = id
        self.iban = iban
        self.account_type = account_type  # e.g., "savings", "checking"
        self.bank_id = bank_id  # Reference to the associated bank
        self.holder_name = holder_name  # Name of the business or entity
        self.address = address  # Address information

    def to_dict(self):
        return {
            "id": self.id,
            "iban": self.iban,
            "accountType": self.account_type,
            "bankId": self.bank_id,
            "holderName": self.holder_name,
            "address": self.address  
        }

# models.py
# models.py

class CreditTransferTransaction:
    def __init__(self, end_to_end_id, amount, currency, creditor_name, creditor_agent_bic, remittance_information):
        self.end_to_end_id = end_to_end_id
        self.amount = amount
        self.currency = currency
        self.creditor_name = creditor_name
        self.creditor_agent_bic = creditor_agent_bic
        self.remittance_information = remittance_information

    def to_dict(self):
        return {
            "EndToEndId": self.end_to_end_id,
            "Amount": {
                "Value": self.amount,
                "Currency": self.currency
            },
            "CreditorAgent": {
                "BIC": self.creditor_agent_bic
            },
            "Creditor": {
                "Name": self.creditor_name
            },
            "RemittanceInformation": {
                "Unstructured": self.remittance_information
            }
        }

class PaymentInformation:
    def __init__(self, payment_info_id, payment_method, batch_booking, number_of_transactions,
                 control_sum, requested_execution_date, debtor_name, debtor_iban,
                 debtor_agent_bic, charge_bearer):
        self.payment_info_id = payment_info_id
        self.payment_method = payment_method
        self.batch_booking = batch_booking
        self.number_of_transactions = number_of_transactions
        self.control_sum = control_sum
        self.requested_execution_date = requested_execution_date
        self.debtor_name = debtor_name
        self.debtor_iban = debtor_iban
        self.debtor_agent_bic = debtor_agent_bic
        self.charge_bearer = charge_bearer
        self.credit_transfer_transactions = []

    def add_credit_transfer_transaction(self, transaction):
        self.credit_transfer_transactions.append(transaction)

    def to_dict(self):
        return {
            "PaymentInfoId": self.payment_info_id,
            "PaymentMethod": self.payment_method,
            "BatchBooking": self.batch_booking,
            "NumberOfTransactions": self.number_of_transactions,
            "ControlSum": self.control_sum,
            "RequestedExecutionDate": self.requested_execution_date,
            "Debtor": {
                "Name": self.debtor_name,
                "Account": {"IBAN": self.debtor_iban},
                "Agent": {"BIC": self.debtor_agent_bic}
            },
            "ChargeBearer": self.charge_bearer,
            "CreditTransferTransactionInformation": [tx.to_dict() for tx in self.credit_transfer_transactions]
        }

class PaymentMessage:
    def __init__(self, message_id, creation_date_time, number_of_transactions, initiating_party_name):
        self.message_id = message_id
        self.creation_date_time = creation_date_time
        self.number_of_transactions = number_of_transactions
        self.initiating_party_name = initiating_party_name
        self.payment_information_list = []

    def add_payment_information(self, payment_info):
        self.payment_information_list.append(payment_info)

    def to_dict(self):
        return {
            "MessageId": self.message_id,
            "CreationDateTime": self.creation_date_time,
            "NumberOfTransactions": self.number_of_transactions,
            "InitiatingParty": {"Name": self.initiating_party_name},
            "PaymentInformation": [info.to_dict() for info in self.payment_information_list]
        }


class PaymentMessageScreening:
    def __init__(self, transaction_id, payment_information, screening_results, screening_status):
        self.transaction_id = transaction_id
        self.payment_information = payment_information
        self.screening_results = screening_results
        self.screening_status = screening_status

    def to_dict(self):
        return {
            "TransactionId": self.transaction_id,
            "PaymentInformation": self.payment_information.to_dict(),
            "ScreeningResults": self.screening_results.to_dict(),
            "ScreeningStatus": self.screening_status.to_dict()
        }


class PaymentInformation:
    def __init__(self, payment_info_id, payment_method, batch_booking, number_of_transactions,
                 control_sum, requested_execution_date, debtor, charge_bearer, credit_transfer_transactions):
        self.payment_info_id = payment_info_id
        self.payment_method = payment_method
        self.batch_booking = batch_booking
        self.number_of_transactions = number_of_transactions
        self.control_sum = control_sum
        self.requested_execution_date = requested_execution_date
        self.debtor = debtor
        self.charge_bearer = charge_bearer
        self.credit_transfer_transactions = credit_transfer_transactions

    def to_dict(self):
        return {
            "PaymentInfoId": self.payment_info_id,
            "PaymentMethod": self.payment_method,
            "BatchBooking": self.batch_booking,
            "NumberOfTransactions": self.number_of_transactions,
            "ControlSum": self.control_sum,
            "RequestedExecutionDate": self.requested_execution_date,
            "Debtor": self.debtor.to_dict(),
            "ChargeBearer": self.charge_bearer,
            "CreditTransferTransactionInformation": [tx.to_dict() for tx in self.credit_transfer_transactions]
        }


class Debtor:
    def __init__(self, name, account, agent):
        self.name = name
        self.account = account
        self.agent = agent

    def to_dict(self):
        return {
            "Name": self.name,
            "Account": self.account.to_dict(),
            "Agent": self.agent.to_dict()
        }


class Account:
    def __init__(self, iban):
        self.iban = iban

    def to_dict(self):
        return {
            "IBAN": self.iban
        }


class Agent:
    def __init__(self, bic):
        self.bic = bic

    def to_dict(self):
        return {
            "BIC": self.bic
        }


class CreditTransferTransaction:
    def __init__(self, end_to_end_id, amount, currency, creditor_name, creditor_agent_bic, remittance_information):
        self.end_to_end_id = end_to_end_id
        self.amount = amount
        self.currency = currency
        self.creditor_name = creditor_name
        self.creditor_agent_bic = creditor_agent_bic
        self.remittance_information = remittance_information

    def to_dict(self):
        return {
            "EndToEndId": self.end_to_end_id,
            "Amount": {
                "Value": self.amount,
                "Currency": self.currency
            },
            "CreditorAgent": {
                "BIC": self.creditor_agent_bic
            },
            "Creditor": {
                "Name": self.creditor_name
            },
            "RemittanceInformation": {
                "Unstructured": self.remittance_information
            }
        }


class ScreeningResults:
    def __init__(self, sanctions_check, high_risk_country_check, amount_threshold_check, suspicious_activity_check):
        self.sanctions_check = sanctions_check
        self.high_risk_country_check = high_risk_country_check
        self.amount_threshold_check = amount_threshold_check
        self.suspicious_activity_check = suspicious_activity_check

    def to_dict(self):
        return {
            "SanctionsCheck": self.sanctions_check.to_dict(),
            "HighRiskCountryCheck": self.high_risk_country_check.to_dict(),
            "AmountThresholdCheck": self.amount_threshold_check.to_dict(),
            "SuspiciousActivityCheck": self.suspicious_activity_check.to_dict()
        }


class SanctionsCheck:
    def __init__(self, flagged_entities, is_sanctioned):
        self.flagged_entities = flagged_entities
        self.is_sanctioned = is_sanctioned

    def to_dict(self):
        return {
            "FlaggedEntities": [entity.to_dict() for entity in self.flagged_entities],
            "IsSanctioned": self.is_sanctioned
        }


class FlaggedEntity:
    def __init__(self, entity_name, flag, reason):
        self.entity_name = entity_name
        self.flag = flag
        self.reason = reason

    def to_dict(self):
        return {
            "EntityName": self.entity_name,
            "Flag": self.flag,
            "Reason": self.reason
        }


class HighRiskCountryCheck:
    def __init__(self, flagged_countries, is_high_risk):
        self.flagged_countries = flagged_countries
        self.is_high_risk = is_high_risk

    def to_dict(self):
        return {
            "FlaggedCountries": [country.to_dict() for country in self.flagged_countries],
            "IsHighRisk": self.is_high_risk
        }


class FlaggedCountry:
    def __init__(self, country_code, flag):
        self.country_code = country_code
        self.flag = flag

    def to_dict(self):
        return {
            "CountryCode": self.country_code,
            "Flag": self.flag
        }


class AmountThresholdCheck:
    def __init__(self, flagged_transactions, is_above_threshold):
        self.flagged_transactions = flagged_transactions
        self.is_above_threshold = is_above_threshold

    def to_dict(self):
        return {
            "FlaggedTransactions": [transaction.to_dict() for transaction in self.flagged_transactions],
            "IsAboveThreshold": self.is_above_threshold
        }


class FlaggedTransaction:
    def __init__(self, transaction_id, flag, threshold, amount):
        self.transaction_id = transaction_id
        self.flag = flag
        self.threshold = threshold
        self.amount = amount

    def to_dict(self):
        return {
            "TransactionId": self.transaction_id,
            "Flag": self.flag,
            "Threshold": self.threshold,
            "Amount": self.amount
        }


class SuspiciousActivityCheck:
    def __init__(self, flagged_transactions, is_suspicious):
        self.flagged_transactions = flagged_transactions
        self.is_suspicious = is_suspicious

    def to_dict(self):
        return {
            "FlaggedTransactions": [transaction.to_dict() for transaction in self.flagged_transactions],
            "IsSuspicious": self.is_suspicious
        }


class ScreeningStatus:
    def __init__(self, status, screening_date, processed_by):
        self.status = status
        self.screening_date = screening_date
        self.processed_by = processed_by

    def to_dict(self):
        return {
            "Status": self.status,
            "ScreeningDate": self.screening_date,
            "ProcessedBy": self.processed_by
        }
