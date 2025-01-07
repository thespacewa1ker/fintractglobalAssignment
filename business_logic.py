# business_logic.py
from model import Bank,Branch,Customer_Bank_Account
import xml.etree.ElementTree as ET
from model import PaymentMessage, PaymentInformation, CreditTransferTransaction
# from model import Payment_Message, Payment_Information, Credit_Transfer_Transaction

def create_bank(data):
    # Create an instance of Bank model with provided data
    bank_instance = Bank(
        id=data["id"],
        name=data["name"],
        country=data["country"],
        street=data["address"]["street"],
        city=data["address"]["city"],
        postal_code=data["address"]["postalCode"],
        phone=data["contact"]["phone"],
        email=data["contact"]["email"],
        legal_entity_identifier=data.get("legalEntityIdentifier", None),
        bic=data.get("bic", None)
    )

    return bank_instance.to_dict()



def create_branch(data):
    # Create an instance of Branch model with provided data
    branch_instance = Branch(
        id=data["id"],
        name=data["name"],
        bank_id=data["bankId"],
        address={
            "street": data["address"]["street"],
            "city": data["address"]["city"],
            "postalCode": data["address"]["postalCode"],
            "country": data["address"]["country"]
        },
        contact={
            "phone": data["contact"]["phone"],
            "email": data["contact"]["email"]
        }
    )

    return branch_instance.to_dict()


def create_customer_bank_account(data):
    # Create an instance of BankAccount model with provided data
    account_instance = Customer_Bank_Account(
        id=data["id"],
        iban=data["iban"],
        account_type=data["accountType"],
        bank_id=data["bankId"],
        holder_name=data["holderName"],
        address=data["address"]  # Capture address information
    )

    return account_instance.to_dict()


def parse_xml_to_payment_message(xml_data: str) -> PaymentMessage:
    root = ET.fromstring(xml_data)
    namespace = {"iso": root.tag.split("}")[0].strip("{")}

    # Extract group header
    grp_hdr = root.find('.//iso:GrpHdr', namespaces=namespace)
    if not grp_hdr:
        raise ValueError("Group header (GrpHdr) not found in XML.")

    payment_message = PaymentMessage(
        message_id=grp_hdr.findtext('iso:MsgId', namespaces=namespace),
        creation_date_time=grp_hdr.findtext('iso:CreDtTm', namespaces=namespace),
        number_of_transactions=grp_hdr.findtext('iso:NbOfTxs', namespaces=namespace),
        initiating_party_name=grp_hdr.findtext('iso:InitgPty/iso:Nm', namespaces=namespace)
    )

    # Extract payment information
    for pmt_inf in root.findall('.//iso:PmtInf', namespaces=namespace):
        payment_info = PaymentInformation(
            payment_info_id=pmt_inf.findtext('iso:PmtInfId', namespaces=namespace),
            payment_method=pmt_inf.findtext('iso:PmtMtd', namespaces=namespace),
            batch_booking=pmt_inf.findtext('iso:BtchBookg', namespaces=namespace) == 'true',
            number_of_transactions=pmt_inf.findtext('iso:NbOfTxs', namespaces=namespace),
            control_sum=pmt_inf.findtext('iso:CtrlSum', namespaces=namespace),
            requested_execution_date=pmt_inf.findtext('iso:ReqdExctnDt', namespaces=namespace),
            debtor_name=pmt_inf.findtext('iso:Dbtr/iso:Nm', namespaces=namespace),
            debtor_iban=pmt_inf.findtext('iso:DbtrAcct/iso:Id/iso:IBAN', namespaces=namespace),
            debtor_agent_bic=pmt_inf.findtext('iso:DbtrAgt/iso:FinInstnId/iso:BIC', namespaces=namespace),
            charge_bearer=pmt_inf.findtext('iso:ChrgBr', namespaces=namespace)
        )

        # Extract credit transfer transaction information
        for cdt_trf in pmt_inf.findall('iso:CdtTrfTxInf', namespaces=namespace):
            transaction = CreditTransferTransaction(
                end_to_end_id=cdt_trf.findtext('iso:PmtId/iso:EndToEndId', namespaces=namespace),
                amount=cdt_trf.findtext('iso:Amt/iso:InstdAmt', namespaces=namespace),
                currency=cdt_trf.find('iso:Amt/iso:InstdAmt', namespaces=namespace).attrib['Ccy'],
                creditor_name=cdt_trf.findtext('iso:Cdtr/iso:Nm', namespaces=namespace),
                creditor_agent_bic=cdt_trf.findtext('iso:CdtrAgt/iso:FinInstnId/iso:BIC', namespaces=namespace),
                remittance_information=cdt_trf.findtext('iso:RmtInf/iso:Ustrd', namespaces=namespace)
            )
            payment_info.add_credit_transfer_transaction(transaction)

        payment_message.add_payment_information(payment_info)

    return payment_message



import xml.etree.ElementTree as ET
from model import PaymentMessageScreening, PaymentInformation, ScreeningResults, ScreeningStatus, \
    CreditTransferTransaction, Debtor, Account, Agent, SanctionsCheck, HighRiskCountryCheck, AmountThresholdCheck, \
    SuspiciousActivityCheck, FlaggedEntity, FlaggedCountry, FlaggedTransaction

# Utility function to parse XML to dictionary
def parse_xml_to_dict(xml_data):
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    
    # Convert the XML to a dictionary
    def parse_element(element):
        parsed_data = {}
        for child in element:
            if len(child) > 0:
                parsed_data[child.tag] = parse_element(child)
            else:
                parsed_data[child.tag] = child.text
        return parsed_data

    return parse_element(root)

# Example function to create PaymentMessageScreening object from parsed XML
def create_payment_message_screening(xml_data):
    try:
        # Step 1: Parse XML into a dictionary
        transaction_data = parse_xml_to_dict(xml_data)
        
        # Step 2: Safely Map the parsed data to the respective data models
        payment_info = PaymentInformation(
            payment_info_id=transaction_data.get('payment_info_id', ''),
            payment_method=transaction_data.get('payment_method', ''),
            batch_booking=transaction_data.get('batch_booking', ''),
            number_of_transactions=transaction_data.get('number_of_transactions', ''),
            control_sum=transaction_data.get('control_sum', ''),
            requested_execution_date=transaction_data.get('requested_execution_date', ''),
            debtor=Debtor(
                name=transaction_data.get('debtor', {}).get('name', ''),
                account=Account(iban=transaction_data.get('debtor', {}).get('account', {}).get('iban', '')),
                agent=Agent(bic=transaction_data.get('debtor', {}).get('agent', {}).get('bic', ''))
            ),
            charge_bearer=transaction_data.get('charge_bearer', ''),
            credit_transfer_transactions=[
                CreditTransferTransaction(
                    end_to_end_id=tx.get('end_to_end_id', ''),
                    amount=tx.get('amount', {}).get('value', ''),
                    currency=tx.get('amount', {}).get('currency', ''),
                    creditor_name=tx.get('creditor', {}).get('name', ''),
                    creditor_agent_bic=tx.get('creditor_agent_bic', ''),
                    remittance_information=tx.get('remittance_information', '')
                ) for tx in transaction_data.get('credit_transfer_transactions', [])
            ]
        )

        # Step 3: Parsing Screening Results with default empty list checks
        screening_results = ScreeningResults(
            sanctions_check=SanctionsCheck(
                flagged_entities=[
                    FlaggedEntity(entity_name=entity.get('entity_name', ''),
                                  flag=entity.get('flag', ''),
                                  reason=entity.get('reason', '')) 
                    for entity in transaction_data.get('screening_results', {}).get('sanctions_check', {}).get('flagged_entities', [])
                ],
                is_sanctioned=transaction_data.get('screening_results', {}).get('sanctions_check', {}).get('is_sanctioned', False)
            ),
            high_risk_country_check=HighRiskCountryCheck(
                flagged_countries=[
                    FlaggedCountry(country_code=country.get('country_code', ''),
                                   flag=country.get('flag', ''))
                    for country in transaction_data.get('screening_results', {}).get('high_risk_country_check', {}).get('flagged_countries', [])
                ],
                is_high_risk=transaction_data.get('screening_results', {}).get('high_risk_country_check', {}).get('is_high_risk', False)
            ),
            amount_threshold_check=AmountThresholdCheck(
                flagged_transactions=[
                    FlaggedTransaction(transaction_id=txn.get('transaction_id', ''),
                                       flag=txn.get('flag', ''),
                                       threshold=txn.get('threshold', ''),
                                       amount=txn.get('amount', ''))
                    for txn in transaction_data.get('screening_results', {}).get('amount_threshold_check', {}).get('flagged_transactions', [])
                ],
                is_above_threshold=transaction_data.get('screening_results', {}).get('amount_threshold_check', {}).get('is_above_threshold', False)
            ),
            suspicious_activity_check=SuspiciousActivityCheck(
                flagged_transactions=[
                    FlaggedTransaction(transaction_id=txn.get('transaction_id', ''),
                                       flag=txn.get('flag', ''),
                                       threshold=txn.get('threshold', ''),
                                       amount=txn.get('amount', ''))
                    for txn in transaction_data.get('screening_results', {}).get('suspicious_activity_check', {}).get('flagged_transactions', [])
                ],
                is_suspicious=transaction_data.get('screening_results', {}).get('suspicious_activity_check', {}).get('is_suspicious', False)
            )
        )

        # Step 4: Parsing Screening Status with empty defaults
        screening_status = ScreeningStatus(
            status=transaction_data.get('screening_status', {}).get('status', ''),
            screening_date=transaction_data.get('screening_status', {}).get('screening_date', ''),
            processed_by=transaction_data.get('screening_status', {}).get('processed_by', '')
        )

        # Step 5: Create the full payment message screening object
        payment_message_screening = PaymentMessageScreening(
            transaction_id=transaction_data.get('transaction_id', ''),
            payment_information=payment_info,
            screening_results=screening_results,
            screening_status=screening_status
        )

        return payment_message_screening

    except Exception as e:
        # Return any exception message if parsing fails
        print(f"Error during payment message screening: {e}")
        return {"error": str(e)}

