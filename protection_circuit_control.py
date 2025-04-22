import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  # Import pandas library
import matplotlib

    
def protection_circuit_control(time_esr_profil = None,time_cap_profil = None,Cap = None,Cap_esr = None,C0 = None,Cap_esr0 = None,ESR_values = None,control_pins_cap = None,control_pins_esr = None): 
    time_step = 2
    
    n_Cap = len(Cap)
    n_ESR = len(ESR_values)
    # based on the offset, the range that chosen by the user should be accordingdly adjusted
    Offset_esr = 0
    Offset_cap = 0
    
    # Adjust time profiles with offsets
    time_cap_offset = np.zeros_like(time_cap_profil)  # Make sure to define the shape based on input
    time_cap_offset[:, 0] = time_cap_profil[:, 0]
    time_cap_offset[:, 1] = time_cap_profil[:, 1] - Offset_cap

    time_esr_offset = np.zeros_like(time_esr_profil)  # Make sure to define the shape based on input
    time_esr_offset[:, 0] = time_esr_profil[:, 0]
    time_esr_offset[:, 1] = time_esr_profil[:, 1] - Offset_esr
    
    ## Step1. Calculate the combinations for capacitors
    total_combinations_Cap = 2 ** n_Cap
    combinations_matrix_Cap = np.zeros((total_combinations_Cap,n_Cap))
    total_Capacitor = np.zeros((total_combinations_Cap,1))
    total_ESR_Cap = np.zeros((total_combinations_Cap,1))
    
    for i in np.arange(0,total_combinations_Cap):
        # Convert the index to binary representation for selecting capacitors
        binary_representation = list(map(int, bin(i)[2:].zfill(n_Cap)))
        combinations_matrix_Cap[i ,:] = binary_representation
        selected_capacities = np.array(Cap)[np.array(binary_representation) == 1]
        selected_ESRs = np.array(Cap_esr)[np.array(binary_representation) == 1]
        # Calculate total capacitance and total ESR for capacitors
        total_Capacitor[i] = sum(selected_capacities) + C0
        if len(selected_ESRs) > 0:
            total_ESR_Cap[i] = 1 / sum(1 / selected_ESRs)
        else:
            total_ESR_Cap[i] = np.inf  # if no ESR values, set to infinity
        
        # Include the base ESR
        total_ESR_Cap[i ] = 1 / (1 / total_ESR_Cap[i] + 1 / Cap_esr0)
    
    Cap_matrix = np.hstack([combinations_matrix_Cap, total_Capacitor, total_ESR_Cap])
    ## Step2: Generate the operation plan for Capacity based on the capacity profile
    # Initialize previous current and result array
    prev_cap = float('nan')
    result_array_cap = [] 
    actual_cap_signal = np.zeros((time_cap_offset.shape[0], 1), dtype=np.uint16)
    N = len(Cap)
    # Loop through each time step in the Capacity profile
    for t in np.arange(0,time_cap_offset.shape[0]):
        cap_target = time_cap_offset[t,1]
        # Check if the current has changed
        if True == True:
            # Find the combination closest to the desired cap
            closest_index  = np.argmin(np.abs(total_Capacitor - cap_target))
            # Store results for this time step
            digital_output = Cap_matrix[closest_index,np.arange(0,N)]
            calculated_cap = Cap_matrix[closest_index,N ]
            calculated_esr = Cap_matrix[closest_index,N + 1]
            active_pins = control_pins_cap[digital_output.astype(bool)]
            # Append to the cell array with time, active pins, and calculated Capacity
            result_array_cap.append([time_cap_offset[t, 0], active_pins, calculated_cap, cap_target, calculated_esr]) 
        
        # Update the actual Capacity signal for the time step
        actual_cap_signal[t] = calculated_cap
        # Update previous Capacity
        prev_cap = cap_target
    
    ### Display Results: Plot Expected and Actual Capacity Signals with Pin Annotations
   ## Plot expected signal (blue solid line)
    #plt.plot(time_cap_offset[:, 0], time_cap_offset[:, 1], 'b-', linewidth=2)
    ## Plot actual signal (red dashed line)
    #plt.plot(time_cap_offset[:, 0], actual_cap_signal, 'r--', linewidth=2)
    ## Plot the given signals provided by the user (green dashed line)
    #plt.plot(time_cap_profil[:, 0], time_cap_profil[:, 1], 'g--', linewidth=2)
    ## Add title and labels with enhanced font
    #plt.title('Expected vs. Measure Cap', fontsize=10, fontweight='bold')
    #plt.xlabel('Time (s)', fontsize=10, fontweight='bold')
    #plt.ylabel('Cap (\muF)', fontsize=10, fontweight='bold')
    ## Add grid with more visual clarity
    #plt.grid(True, linestyle=':', color='k', alpha=0.6)
    #plt.tick_params(axis='both', labelsize=10)
    ## Add legends with location and enhanced appearance
    #plt.legend(['User-defined Cap considering offset', 'Selected Cap', 'User-defined Cap'], loc='lower left', fontsize=10)
    ### Display pin numbers at Capacity changes
    ## for k = 1:length(result_array_cap)
    ##     t_time = result_array_cap{k, 1}; # Time of the change
    ##     active_pins_str = num2str(result_array_cap{k, 2}); # Convert active pins to string for annotation
    ##     t_current = result_array_cap{k, 3}; # Corresponding Capacity
    ##     text(t_time, t_current + 1.5, ['Pins: ' active_pins_str], 'FontSize', 8, 'Color', 'k', 'FontWeight', 'bold'); # Annotate pin numbers
    ## end
    ## Show plot
   # plt.show()
    ## Convert the result array to a DataFrame for better readability
    #result_table_cap = pd.DataFrame(result_array_cap, columns=['Time', 'Active_Pins_cap', 'Cap', 'Target Cap', 'Cap_esr'])
    ## Display the result table
    #print(result_table_cap)
    
    ## Step3. Calculate combinations for resistors
    total_combinations_ESR = 2 ** n_ESR
    combinations_matrix_ESR = np.zeros((total_combinations_ESR,n_ESR))
    total_ESR = np.zeros((total_combinations_ESR,1))
    
    for i in np.arange(0,total_combinations_ESR):
        binary_representation = np.array(list(np.binary_repr(i, n_ESR)), dtype=int)
        combinations_matrix_ESR[i ,:] = binary_representation
        selected_ESRs = ESR_values[binary_representation == 1]
        if selected_ESRs.size > 0:
            total_ESR[i] = 1 / np.sum(1 / selected_ESRs)  # Parallel combination of resistors
        else:
            total_ESR[i] = np.inf
    
    ## Step 4:  Take the ESR of Capacity into consideration: The presented ESR of the
    # combination(temp) sit the sum of the esr-combi und the cap_esr_combi
    ESR_matrix = np.column_stack((combinations_matrix_ESR, total_ESR))    
    time_esr_profil_consider_cap = np.zeros((time_esr_offset.shape[0], 2))
    time_esr_profil_consider_cap[:,0] = time_esr_offset[:,0]
    time_esr_profil_consider_cap[:, 1] = time_esr_offset[:, 1] - [row[4] for row in result_array_cap]
    
    ## Step 5: Generate the operation plan for ESR based on the resistors profile under consideration of ESR of Capacity
    # Initialize previous resistors and result array
    prev_cap = float('nan')
    result_array_esr = []
    actual_esr_signal = np.zeros((time_esr_profil_consider_cap.shape[0],1), dtype=np.uint16)
    N = len(ESR_values)
    # Loop through each time step in the resistors profile
    for t in np.arange(0,time_esr_profil_consider_cap.shape[0]):
        esr_target = time_esr_profil_consider_cap[t,1]
        # Check if the resistors has changed
        if True == True:
            # Find the combination closest to the desired ESR
            closest_index = np.argmin(np.abs(ESR_matrix[:,8] - esr_target))
            # Store results for this time step
            digital_output = ESR_matrix[closest_index,np.arange(0,N)]
            active_pins = control_pins_esr[digital_output.astype(bool)]
            # Append to the cell array with time, active pins, and calculated resistors
            result_array_esr.append([time_esr_offset[t, 0], 
                                     active_pins,
                                     ESR_matrix[closest_index,-1],
                                     result_array_cap[t][4], 
                                     ESR_matrix[closest_index,-1]+result_array_cap[t][4], 
                                     time_esr_offset[t,1]]) 
        # Update previous resistors
        prev_esr = esr_target
    
    matplotlib.use('Agg')  # Verhindert GUI-Probleme mit Matplotlib
    # Plot expected signal (blue solid line)
    plt.plot([row[0] for row in result_array_esr], [row[5] for row in result_array_esr], 'b-', linewidth=2)
    # Plot chosen signal (red dashed line)
    plt.plot([row[0] for row in result_array_esr], [row[4] for row in result_array_esr], 'r--', linewidth=2)
    # Plot the given signals provided by the user (green dashed line)
    plt.plot([row[0] for row in time_esr_profil], [row[1] for row in time_esr_profil], 'g--', linewidth=2)
    # Add title and labels with enhanced font
    plt.title('Expected vs. Measured Resistance', fontsize=10, fontweight='bold')
    plt.xlabel('Time (s)', fontsize=10, fontweight='bold')
    plt.ylabel('Resistance (mΩ)', fontsize=10, fontweight='bold')
    # Add grid with more visual clarity
    plt.grid(True, linestyle=':', color='k', alpha=0.6)
    plt.tick_params(axis='both', labelsize=10)
    # Add legends with location and enhanced appearance
    plt.legend(['User-defined Resistance considering offset', 'Selected Resistance', 'User-defined Resistance'], 
            loc='lower left', fontsize=10)
    # Show the plot
    plt.show()

    # Convert result_array_esr to a pandas DataFrame for better readability
    column_names = ['Time', 'Active_Pins_esr', 'Combi of ESR', 'Resistance of Cap', 'Realizable Resistance', 'Target Resistance']
    result_table_esr = pd.DataFrame(result_array_esr, columns=column_names)

    # Display the result table
    print(result_table_esr)
    
    ## summerize all the result_arrays together
    result_array_cap = np.array(result_array_cap, dtype=object)
    result_array_esr = np.array(result_array_esr, dtype=object)
    result_array = result_array_cap
    result_array = np.hstack((result_array_cap, result_array_esr[:, 1:])) 
    column_names = [
        "Time", "Active_Pins_cap", "realizable Cap", "Target Cap", "Cap_esr",
        "Active_Pins_esr", "combi of ESR", "Resistance of Cap", "realizable Resistance", "Target_Resistance"]
    result_table = pd.DataFrame(result_array, columns=column_names)    
    result_table.drop(columns=["Resistance of Cap"], inplace=True)    
    all_pin = np.array([control_pins_cap,control_pins_esr])
    # Kombinieren von Active_Pins_cap und Active_Pins_esr in eine einzige Liste pro Zeile
    
    return result_table
    
