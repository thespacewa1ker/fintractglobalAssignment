from flask import Flask, request, jsonify
from flasgger import Swagger
from business_logic import create_bank, create_branch, create_customer_bank_account, parse_xml_to_payment_message,create_payment_message_screening
import xml.etree.ElementTree as ET

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/create_bank', methods=['POST'])
def create_bank_endpoint():
    """
    Create a new bank.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: BankInput
          properties:
            id:
              type: string
              example: HSBC001
            name:
              type: string
              example: HSBC Holdings plc
            country:
              type: string
              example: GB
            address:
              type: object
              properties:
                street:
                  type: string
                  example: 8 Canada Square
                city:
                  type: string
                  example: London
                postalCode:
                  type: string
                  example: E14 5HQ
            contact:
              type: object
              properties:
                phone:
                  type: string
                  example: +44 20 7991 8888
                email:
                  type: string
                  example: contact@hsbc.com
            legalEntityIdentifier:
              type: string
              example: LEI123456789
            bic:
              type: string
              example: BANKDEFFXXX

    responses:
      201:
        description: Bank created successfully.
      400:
        description: Invalid input.
    """
    data = request.json  # Get JSON data from request

    try:
        # Call create_bank with the incoming data
        bank_info = create_bank(data)

        # Here you would typically save the bank instance to a database

        # Return created bank information with 201 status
        return jsonify(bank_info), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Handle errors


@app.route('/create_customer_account', methods=['POST'])
def create_account_endpoint():
    """
    Create a new bank account.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: AccountInput
          properties:
            id:
              type: string
              example: AC001
            iban:
              type: string
              example: DE75512108001245126162
            accountType:
              type: string
              example: savings
            bankId:
              type: string
              example: HSBC001
            holderName:
              type: string
              example: John Doe
            address:
              type: object
              properties:
                street:
                  type: string
                  example: 8 Canada Square
                city:
                  type: string
                  example: London
                postalCode:
                  type: string
                  example: E14 5HQ
                country:
                  type: string
                  example: GB

    responses:
      201:
        description: Account created successfully.
      400:
        description: Invalid input.
    """
    data = request.json  # Get JSON data from request

    try:
        # Call create_account with the incoming data
        account_info = create_customer_bank_account(data)

        # Here you would typically save the account instance to a database

        # Return created account information with 201 status
        return jsonify(account_info), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Handle errors


@app.route('/create_branch', methods=['POST'])
def create_branch_endpoint():
    """
    Create a new branch.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: BranchInput
          properties:
            id:
              type: string
              example: BR001
            name:
              type: string
              example: HSBC London Branch
            bankId:
              type: string
              example: HSBC001
            address:
              type: object
              properties:
                street:
                  type: string
                  example: 8 Canada Square
                city:
                  type: string
                  example: London
                postalCode:
                  type: string
                  example: E14 5HQ
                country:
                  type: string
                  example: GB
            contact:
              type: object
              properties:
                phone:
                  type: string
                  example: "+44 20 7991 8888"
                email:
                  type: string
                  example: contact@hsbc.com

    responses:
      201:
        description: Branch created successfully.
      400:
        description: Invalid input.
    """
    data = request.json  # Get JSON data from request

    try:
        # Call create_branch with the incoming data
        branch_info = create_branch(data)

        # Here you would typically save the branch instance to a database

        # Return created branch information with 201 status
        return jsonify(branch_info), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Handle errors


@app.route('/payment_messages', methods=['POST'])
def payment_messages():
    """
    Upload XML data to create payment messages.
    ---
    tags:
      - Payment Messages
    parameters:
      - name: xml_data
        in: body
        type: string
        required: true
        description: The XML data containing payment information.
    responses:
      201:
        description: A JSON object containing the parsed payment messages.
      400:
        description: Error due to invalid input or parsing issues.
      500:
        description: Unexpected error occurred.
    """
    
    # Get the XML data from the request body.
    xml_data = request.data.decode('utf-8')

    if not xml_data.strip():
        return jsonify({"error": "No XML data provided"}), 400
    
    try:
         # Parse the XML to create a PaymentMessage object and convert to JSON format.
         payment_message = parse_xml_to_payment_message(xml_data)

         # Convert to JSON response format.
         response_data = payment_message.to_dict()

         return jsonify({"PaymentMessages": [response_data]}), 201

    except Exception as e:
         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    


@app.route('/screen-payment-message', methods=['POST'])
def screen_payment_message():
    """
    Screen a payment message.
    ---
    tags: 
      - Payment Messages
    parameters: 
      - name: xml_data
        in: body
        type: string
        required: true        
        description: The XML data containing payment information. The XML should conform to the schema defined for payment messages.
    requestBody:
      content:
        application/xml:
          schema:
            type: string
            description: XML formatted data containing payment details, screening results, and transaction information.
    responses:  
      200:
        description: A JSON object containing the parsed and processed payment message information.
        content:
          application/json:
            schema:
              type: object
              properties:
                transaction_id:
                  type: string
                  description: Unique identifier for the payment transaction.
                payment_information:
                  type: object
                  properties:
                    payment_info_id:
                      type: string
                    payment_method:
                      type: string
                    batch_booking:
                      type: boolean
                    number_of_transactions:
                      type: integer
                    control_sum:
                      type: number
                    requested_execution_date:
                      type: string
                      format: date
                    debtor:
                      type: object
                      properties:
                        name:
                          type: string
                        account:
                          type: object
                          properties:
                            iban:
                              type: string
                        agent:
                          type: object
                          properties:
                            bic:
                              type: string
                    charge_bearer:
                      type: string
                    credit_transfer_transactions:
                      type: array
                      items:
                        type: object
                        properties:
                          end_to_end_id:
                            type: string
                          amount:
                            type: object
                            properties:
                              value:
                                type: number
                              currency:
                                type: string
                          creditor:
                            type: object
                            properties:
                              name:
                                type: string
                          creditor_agent_bic:
                            type: string
                          remittance_information:
                            type: string
                screening_results:
                  type: object
                  properties:
                    sanctions_check:
                      type: object
                      properties:
                        flagged_entities:
                          type: array
                          items:
                            type: object
                            properties:
                              entity_name:
                                type: string
                              flag:
                                type: string
                              reason:
                                type: string
                        is_sanctioned:
                          type: boolean
                    high_risk_country_check:
                      type: object
                      properties:
                        flagged_countries:
                          type: array
                          items:
                            type: object
                            properties:
                              country_code:
                                type: string
                              flag:
                                type: string
                        is_high_risk:
                          type: boolean
                    amount_threshold_check:
                      type: object
                      properties:
                        flagged_transactions:
                          type: array
                          items:
                            type: object
                            properties:
                              transaction_id:
                                type: string
                              flag:
                                type: string
                              threshold:
                                type: number
                              amount:
                                type: number
                        is_above_threshold:
                          type: boolean
                    suspicious_activity_check:
                      type: object
                      properties:
                        flagged_transactions:
                          type: array
                          items:
                            type: object
                            properties:
                              transaction_id:
                                type: string
                              flag:
                                type: string
                              threshold:
                                type: number
                              amount:
                                type: number
                        is_suspicious:
                          type: boolean
                screening_status:
                  type: object
                  properties:
                    status:
                      type: string
                    screening_date:
                      type: string
                      format: date
                    processed_by:
                      type: string
      400:
        description: Invalid XML input or parsing issues.
      500:  
        description: Unexpected error occurred.
    """
    try:
        # Get the XML data from the request
        xml_data = request.data.decode('utf-8')

        # Process the XML data using the business logic function
        payment_message_screening = create_payment_message_screening(xml_data)

        # Return the result as JSON
        return jsonify(payment_message_screening.to_dict()), 200
    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
     app.run()
