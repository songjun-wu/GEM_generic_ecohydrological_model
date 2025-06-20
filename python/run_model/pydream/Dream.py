# -*- coding: utf-8 -*-

import os
import numpy as np
import random
from . import Dream_shared_vars
from datetime import datetime
import traceback
import time
from mpi4py import MPI

class Dream:
    """An implementation of the MT-DREAM\ :sub:`(ZS)`\  algorithm introduced in:
        Laloy, E. & Vrugt, J. A. High-dimensional posterior exploration of hydrologic models using multiple-try DREAM\ :sub:`(ZS)`\  and high-performance computing. Water Resources Research 48, W01526 (2012).
    
    Parameters
    ----------
    variables : iterable of instance(s) of SampledParam class
        Model parameters to be sampled with specified prior.
    nseedchains : int
        Number of draws with which to initialize the DREAM history.  Default = 10 * n dimensions
    nCR : int
        Number of crossover values to sample from during run (and to fit during crossover burn-in period).  Default = 3
    adapt_crossover : bool
        Whether to adapt crossover values during the burn-in period.  Default is to adapt.
    crossover_burnin : int
        Number of iterations to fit the crossover values.  Defaults to 10% of total iterations.
    DEpairs : int or list
        Number of chain pairs to use for crossover and selection of next point.  Default = 1.  Can pass a list to have a random number of pairs selected every iteration.
    lamb : float
        e sub d in DREAM papers.  Random error for ergodicity.  Default = .05
    zeta : float
        Epsilon in DREAM papers.  Randomization term. Default = 1e-12
    history_thin : int
        Thinning rate for history to reduce storage requirements.  Every n-th iteration will be added to the history.
    snooker : float
        Probability of proposing a snooker update.  Default is .1.  To forego snooker updates, set to 0.
    p_gamma_unity : float
        Probability of proposing a point with gamma=unity (i.e. a point relatively far from the current point to enable jumping between disconnected modes).  Default = .2.
    start_random : bool
        Whether to intialize chains from a random point in parameter space drawn from the prior (default = yes).  Will override starting position set when sample was called, if any.
    save_history : bool
        Whether to save the history to file at the end of the run (essential if you want to continue the run).  Default is yes.
    history_file : str
        Name of history file to be loaded.  Assumed to be in directory you ran the script from.  If False, no file to be loaded.
    crossover_file : str
        Name of crossover file to be loaded. Assumed to be in directory you ran the script from.  If False, no file to be loaded.
    multitry : bool
        Whether to utilize multi-try sampling.  Default is no.  If set to True, will be set to 5 multiple tries.  Can also directly specify an integer if desired.
    parallel : bool
        Whether to run multi-try samples in parallel (using multiprocessing).  Default is false.  Irrelevant if multitry is set to False.
    verbose : bool
        Whether to print verbose progress.  Default is false.
    model_name : str
        A model name to be used as a prefix when saving history and crossover value files.
    hardboundaries : bool
        Whether to relect point back into bounds of hard prior (i.e., if using a uniform prior, reflect points outside of boundaries back in, so you don't waste time looking at points with logpdf = -inf).
    mp_context : multiprocessing context or None.
        Method used to to start the processes. If it's None, the default context, which depends in Python version and OS, is used.
        For more information please check: https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
    """

    def __init__(self, model, variables=None, nseedchains=None, nCR=3, adapt_crossover=True, adapt_gamma=False,
                 crossover_burnin=None, DEpairs=1, lamb=.05, zeta=1e-12, history_thin=10, snooker=.10,
                 p_gamma_unity=.20, gamma_levels=1, start_random=True, save_history=True, history_file=False,
                 crossover_file=False, gamma_file=False, multitry=False, parallel=False, verbose=False,
                 model_name=False, hardboundaries=True, **kwargs):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

        # Set model and variable attributes (if no variables passed, set to all parameters)
        self.model = model
        self.model_name = model_name
        if variables is None:
            self.variables = self.model.sampled_parameters
        else:
            self.variables = variables

        #Calculate total variable dimension and set boundaries
        self.boundaries = hardboundaries
        self.total_var_dimension = 0
        for var in self.variables:
            self.total_var_dimension += var.dsize

        #Set min and max values for boundaries
        if self.boundaries:
            if self.total_var_dimension == 1:
                self.boundary_mask = True
            else:
                self.boundary_mask = np.ones((self.total_var_dimension), dtype=bool)
            self.mins = []
            self.maxs = []
            n = 0
            for var in self.variables:
                interval = var.interval(1)

                if var.dsize > 1:
                    self.mins += list(interval[0])
                    self.maxs += list(interval[1])
                else:
                    self.mins.append(interval[0])
                    self.maxs.append(interval[1])
                n += var.dsize
            self.mins = np.array(self.mins)
            self.maxs = np.array(self.maxs)
        
        self.nseedchains = nseedchains
        self.nCR = nCR

        #If the number of crossover values is greater than the total variable dimension, set it to be the total variable dimension
        if self.nCR > self.total_var_dimension:
            self.nCR = self.total_var_dimension
            print('Warning: the total number of crossover values specified ('+str(nCR)+') is less than the total dimension of all variables ('+str(self.total_var_dimension)+').  Setting the number of crossover values to be equal to the total variable dimension.')

        #If there is only one variable dimension, don't adapt crossover values
        if self.total_var_dimension == 1 and adapt_crossover:
            adapt_crossover = False
            print('Warning: the total variable dimension = 1, so crossover values will not be adapted, even though crossover adaptation was requested.')

        self.ngamma = gamma_levels
        self.njoint_cr_gamma_probs = nCR*gamma_levels
        self.crossover_burnin = crossover_burnin
        self.crossover_file = crossover_file

        self.adapt_crossover = adapt_crossover

        #Load crossover values from file if given, else set to 1/nCR for all and adapt if requested
        if crossover_file:
            self.CR_probabilities = np.load(crossover_file)
            self.nCR = len(self.CR_probabilities)
            if self.adapt_crossover:
                print('Warning: Crossover values loaded and adapt_crossover = True.  Crossover values will be further adapted.')
        else:
            self.CR_probabilities = [1/float(self.nCR) for i in range(self.nCR)]

        #Load gamma values from file if given, otherwise set to 1/ngamma for all
        self.adapt_gamma = adapt_gamma
        if gamma_file:
            self.gamma_probabilities = np.load(gamma_file)
            if adapt_gamma:
                print('Warning: Gamma values loaded and adapt gamma = True.  Gamma values will be further adapted.')
        else:
            self.gamma_probabilities = [1/float(self.ngamma) for i in range(self.ngamma)]
        
        #Set crossover values and gamma (the proportion of dimensions to crossover/gamma level to choose)
        self.CR_values = np.array([m/float(self.nCR) for m in range(1, self.nCR+1)])  
        self.gamma_level_values = np.array([m for m in range(1, self.ngamma+1)])

        #Set number of pairs to use for determining distance between points for proposals
        self.DEpairs = np.linspace(1, DEpairs, num=DEpairs, dtype=int) #This is delta in original Matlab code

        self.snooker = snooker
        self.p_gamma_unity = p_gamma_unity

        #If no multitry requested, set value to 1, if requested without a value, set to 5, else set to the value passed
        if multitry == False:
            self.multitry = 1
        elif multitry == True:
            self.multitry = 5
        else:
            self.multitry = multitry

        self.parallel = parallel
        self.lamb = lamb #This is e sub d in DREAM papers
        self.zeta = zeta #This is epsilon in DREAM papers
        self.last_logp = None

        #Set the number of seedchains to 10*dimensions to fit
        if self.nseedchains == None:
            #self.nseedchains = self.total_var_dimension*10
            self.nseedchains = self.total_var_dimension * 2

        #Set array of gamma values (decreasing step size with increasing level)
        gamma_array = np.zeros((self.ngamma, DEpairs, self.total_var_dimension))
        gamma_level_decrease = 1
        for gamma_level in range(1, self.ngamma+1):         
            for delta in range(1, DEpairs+1):
                gamma_array[gamma_level-1, delta-1, :] = (2.38 / np.sqrt(2*delta*np.linspace(1, self.total_var_dimension, num=self.total_var_dimension)))/gamma_level_decrease
            gamma_level_decrease = gamma_level_decrease*2
        self.gamma_arr = gamma_array
        self.gamma = None

        self.iter = 0
        self.local_burn_in = 0

        self.local_count = 0
        self.global_count = 0

        

        self.chain_n = None
        self.nchains = None
        self.len_history = 0
        self.save_history = save_history
        self.history_file = history_file
        self.history_thin = history_thin
        self.start_random = start_random
        self.verbose = verbose
        self.logp = self.model.total_logp
    
    def astep(self, q0, chainID, modelID, nchains, total_iterations, T=1., last_loglike=None, last_logprior=None):

        # On first iteration, check that shared variables have been initialized (which only occurs if multiple chains have been started).
        if self.iter == 0:
            try:
                # Chain layout
                self.chainID = chainID
                self.modelID = modelID
                self.chain_n = chainID
                self.nchains = nchains
                
                # Intra-chain communicator (5 ranks per chain)
                self.subcomm = self.comm.Split(color=chainID, key=self.rank)
                self.subrank = self.subcomm.Get_rank()
                
                # Inter-chain communicator (only chain masters)
                self.is_chain_master = (self.modelID == 0)
                self.master_comm = self.comm.Split(color=0 if self.is_chain_master else MPI.UNDEFINED, key=self.rank)
                
                # Allocate full shared history array on rank 0 of master_comm
                if self.is_chain_master:
                    Dream_shared_vars.win_history = MPI.Win.Create(Dream_shared_vars.history, comm=self.master_comm)
                    Dream_shared_vars.win_history.Fence()
                else:
                    Dream_shared_vars.win_history = None
                    history = None

                if self.rank == 0 and not self.history_file and Dream_shared_vars.history_seeded == b'F':

                    for i in range(self.nseedchains):
                        start_loc = i * self.total_var_dimension
                        end_loc = start_loc + self.total_var_dimension
                        init_arr = self.draw_from_prior(self.variables)           
                        Dream_shared_vars.history[start_loc:end_loc] = init_arr
                    Dream_shared_vars.history_seeded = b'T'
                if self.is_chain_master:   
                    #Dream_shared_vars.win_history.Lock(0)
                    Dream_shared_vars.win_history.Get(Dream_shared_vars.history, target_rank=0, target=0)
                    #Dream_shared_vars.win_history.Unlock(0)
                    Dream_shared_vars.win_history.Fence()
                     
                    
                    #Dream_shared_vars.history = self.comm.bcast(Dream_shared_vars.history, root=0)
                    
                    if self.start_random:
                        q0 = self.draw_from_prior(self.variables, random_seed=True)

                    # Also get length of history array so we know when to save it at end of run.
                    if self.save_history:
                        self.len_history = len(np.frombuffer(Dream_shared_vars.history))

                    

                    print('DREAM initialisation done for chain '+str(self.chainID)+' model '+str(self.modelID), flush=True)

                
                Dream_shared_vars.history_seeded = self.comm.bcast(Dream_shared_vars.history_seeded, root=0)
                self.crossover_burnin = self.comm.bcast(self.crossover_burnin, root=0)

                    
            except Exception as e:
                print('Error found in the DREAM initialisation :   ', e, flush=True)

            #except AttributeError:
            #    raise Exception('Dream should be run with multiple chains in parallel.  Set nchains > 1.')          
        
        try:
            
            if last_loglike != None:
                self.last_like = last_loglike
                self.last_prior = last_logprior
                self.last_logp = T*self.last_like + self.last_prior
            
            if self.is_chain_master:        
                #Determine whether to run snooker update or not for this iteration.
                run_snooker = self.set_snooker()
                
        
                #Set crossover value for generating proposal point
                CR = self.set_CR(self.CR_probabilities, self.CR_values)
                
                #Set DE pair choice to be used for generating proposal point for this iteration.
                DEpair_choice = self.set_DEpair(self.DEpairs)

                #Select gamma size level
                gamma_level = self.set_gamma_level(self.gamma_probabilities, self.gamma_level_values)
            

                #Generate proposal points
                if not run_snooker:
                    proposed_pts = self.generate_proposal_points(self.multitry, q0, CR, DEpair_choice, gamma_level, snooker=False)              
                else:
                    proposed_pts, snooker_logp_prop, z = self.generate_proposal_points(self.multitry, q0, CR, DEpair_choice, gamma_level, snooker=True)                 

            # Broadcast proposed params to all model ranks in this chain
            q0 = self.subcomm.bcast(q0, root=0)
            if self.last_logp == None:
                self.last_prior, self.last_like = self.logp(q0, self.chainID, self.modelID, total_iterations)
                # Gather results from model ranks
                all_likes = self.subcomm.gather(self.last_like, root=0)
                if self.is_chain_master:
                    self.last_like = np.log(np.sum(all_likes)) * (-1*500)
                self.last_logp = T*self.last_like + self.last_prior
            
            

            #Evaluate proposed samples(s)
            proposed_pts = proposed_pts if self.is_chain_master else None
            proposed_pts = self.subcomm.bcast(proposed_pts, root=0)
            q_prior, q_loglike_noT = self.logp(np.squeeze(proposed_pts), self.chainID, self.modelID, total_iterations)
            # Gather results from model ranks
            all_likes = self.subcomm.gather(q_loglike_noT, root=0)
            if self.is_chain_master:
                q_loglike_noT = np.log(np.sum(all_likes)) * (-1*500)
            q_logp_noT = q_prior + q_loglike_noT
            q_logp = T*q_loglike_noT + q_prior
            q = np.squeeze(proposed_pts)
            
            
            # Sample evaluation
            if self.is_chain_master:
                if run_snooker:
                    total_proposed_logp = q_logp + snooker_logp_prop
                    norm = np.linalg.norm(q0 - z)
                    snooker_current_logp = np.log(norm, where=norm != 0) * (self.total_var_dimension - 1)
                    total_old_logp = self.last_logp + snooker_current_logp
                    q_new = metrop_select(np.nan_to_num(total_proposed_logp - total_old_logp), q, q0)
                else:
                    q_new = metrop_select(np.nan_to_num(q_logp) - np.nan_to_num(self.last_logp), q, q0)
                
                if not np.array_equal(q0, q_new):
                    self.last_logp = q_logp_noT
                    self.last_prior = q_prior
                    self.last_like = q_loglike_noT
                
            
            if self.is_chain_master:
                #Place new point in history given history thinning rate
                
                if self.iter % self.history_thin == 0 or self.iter == (self.niterations - 1):
                    self.global_count = self.record_history(self.nseedchains, self.total_var_dimension, q_new, self.len_history)  
                if self.iter < self.crossover_burnin+1:
                    self.set_current_position_arr(self.total_var_dimension, q_new)

                #If adapting crossover values, estimate ideal crossover probabilities for each dimension during burn-in.
                #Don't do this for the first 10 iterations to give all chains a chance to fill in the shared current position array
                #Don't count iterations where gamma was set to 1 in crossover adaptation calculations
                if self.adapt_crossover and self.iter > 10 and self.iter < self.crossover_burnin and not np.any(np.array(self.gamma) == 1.0):
                    #If a snooker update was run, then regardless of the originally selected CR, a CR=1.0 was used.
                    if not run_snooker:
                        self.CR_probabilities = self.estimate_crossover_probabilities(self.total_var_dimension, q0, q_new, CR)
                    else:
                        self.CR_probabilities = self.estimate_crossover_probabilities(self.total_var_dimension, q0, q_new, CR=1)

                
                if self.adapt_gamma and self.iter > 10 and self.iter < self.crossover_burnin and not np.any(np.array(self.gamma) == 1.0) and not run_snooker:
                    self.gamma_probabilities = self.estimate_gamma_level_probs(self.total_var_dimension, q0, q_new, gamma_level)
                
                

                if self.iter == self.crossover_burnin:
                    
                    self.master_comm.Barrier()
                    self.local_burn_in = 1

                    
                    
                    total_burn_in = self.master_comm.allreduce(self.local_burn_in, op=MPI.SUM)
                    
                    #if self.rank == 0:
                    #    Dream_shared_vars.nchains = total_burn_in
                    #total_burn_in = self.comm.bcast(total_burn_in, root=0)
                    
                    if self.adapt_gamma:
                        self.gamma_probabilities = self.estimate_gamma_level_probs(self.total_var_dimension, q0, q_new, gamma_level)
                    
                    if self.adapt_crossover:
                        #If a snooker update was run, then regardless of the originally selected CR, a CR=1.0 was used.
                        if not run_snooker:
                            self.CR_probabilities = self.estimate_crossover_probabilities(self.total_var_dimension, q0, q_new, CR)
                        else:
                            self.CR_probabilities = self.estimate_crossover_probabilities(self.total_var_dimension, q0, q_new, CR=1)
                    

                    while total_burn_in != self.nchains:
                        time.sleep(3)
                        total_burn_in = self.comm.allreduce(self.local_burn_in, op=MPI.SUM)  
                    time.sleep(5)

                    if self.adapt_gamma:
                        self.gamma_probabilities = self.master_comm.bcast(self.gamma_probabilities, root=0)

                        
                    if self.adapt_crossover:
                        self.CR_probabilities = self.master_comm.bcast(self.CR_probabilities, root=0)
                    
            
            q_new = q_new if self.is_chain_master else None
                                
            self.iter += 1
            
        except Exception as e:
            traceback.print_exc()
            raise e
        return q_new, self.last_prior, self.last_like, self.is_chain_master
        
    def set_current_position_arr(self, ndimensions, q_new):
        """Add current position of chain to shared array available to other chains.

        Parameters
        ----------
        ndimensions : int
            number of dimensions in a draw

        q_new : numpy array
            accepted point in parameter space
        """
        
        if self.nchains == None:
            current_positions = Dream_shared_vars.current_positions
            self.nchains = len(current_positions)//ndimensions
        
        if self.chain_n == None:
            self.chain_n = Dream_shared_vars.nchains-1
            Dream_shared_vars.nchains -= 1
        
        #We only need to have the current position of all chains for estimating the crossover probabilities during burn-in so don't bother updating after that
        if self.iter < self.crossover_burnin+1:
            start_cp = int(self.chain_n*ndimensions)
            end_cp = int(start_cp + ndimensions)
            Dream_shared_vars.current_positions[start_cp:end_cp] = np.array(q_new).flatten()        
        
    def estimate_crossover_probabilities(self, ndim, q0, q_new, CR):
        """Adapt crossover probabilities during crossover burn-in period.

        Parameters
        ----------
        ndim : int
            number of dimensions in a draw
        q0 : numpy array
            original point in parameter space
        q_new : numpy array
            new point in parameter space
        CR : float
            selected crossover probability for this step"""

        cross_probs = Dream_shared_vars.cross_probs[0:self.nCR]
        
        #Compute squared normalized jumping distance
        m_loc = int(np.where(self.CR_values == CR)[0])

        Dream_shared_vars.ncr_updates[m_loc] += 1
        
        current_positions = Dream_shared_vars.current_positions.reshape((self.nchains, ndim))
        
        sd_by_dim = np.std(current_positions, axis=0)

        #Replace any zeros in sd array with a very small number to avoid division by zero errors
        sd_by_dim[sd_by_dim == 0] = 1e-12
        
        change = np.nan_to_num(np.sum(((q_new - q0)/sd_by_dim) ** 2))
        
        Dream_shared_vars.delta_m[m_loc] = Dream_shared_vars.delta_m[m_loc] + change
        
        #Update probabilities of tested crossover value        
        #Leave probabilities unchanged until all possible crossover values have had at least one successful move so that a given value's probability isn't prematurely set to 0, preventing further testing.
        delta_ms = Dream_shared_vars.delta_m[0:self.nCR]
        ncr_updates = Dream_shared_vars.ncr_updates[0:self.nCR]
        
        if np.all(delta_ms != 0) == True:
            for m in range(self.nCR):
                cross_probs[m] = (Dream_shared_vars.delta_m[m] / Dream_shared_vars.ncr_updates[m])*self.nchains
            cross_probs = cross_probs / np.sum(cross_probs)
        
        Dream_shared_vars.cross_probs[0:self.nCR] = cross_probs
        
        self.CR_probabilities = cross_probs
        
        return cross_probs
    
    def estimate_gamma_level_probs(self, ndim, q0, q_new, gamma_level):
        """Adapt gamma level probabilities during burn-in

        Parameters
        ----------
        ndim : int
            number of dimensions in a draw
        q0 : numpy array
            original point in parameter space
        q_new : numpy array
            new point in parameter space
        gamma_level : int
            gamma level selected for this step"""

        current_positions = Dream_shared_vars.current_positions

        current_positions = current_positions.reshape((self.nchains, ndim))

        sd_by_dim = np.std(current_positions, axis=0)
        
        gamma_level_probs = Dream_shared_vars.gamma_level_probs[0:self.ngamma]
            
        gamma_loc = int(np.where(self.gamma_level_values == gamma_level)[0])
            
        Dream_shared_vars.ngamma_updates[gamma_loc] += 1
            
        Dream_shared_vars.delta_m_gamma[gamma_loc] = Dream_shared_vars.delta_m_gamma[gamma_loc] + np.nan_to_num(np.sum(((q_new - q0)/sd_by_dim)**2))
    
        delta_ms_gamma = Dream_shared_vars.delta_m_gamma[0:self.ngamma]
            
        if np.all(delta_ms_gamma != 0) == True:
            for m in range(self.ngamma):
                gamma_level_probs[m] = (Dream_shared_vars.delta_m_gamma[m] / Dream_shared_vars.ngamma_updates[m]) * self.nchains
            gamma_level_probs = gamma_level_probs / np.sum(gamma_level_probs)
        Dream_shared_vars.gamma_level_probs[0:self.ngamma] = gamma_level_probs
        return gamma_level_probs
    
    def set_snooker(self):
        """Choose to run a snooker update on a given iteration or not."""
        if self.snooker != 0:
            snooker_choice = np.where(np.random.multinomial(1, [self.snooker, 1 - self.snooker]) == 1)  # throw the dice only once, return = [chances of getting the first option, ... of the second option]
                
            if snooker_choice[0] == 0:
                run_snooker = True
            else:
                run_snooker = False
        else:
            run_snooker = False
            
        return run_snooker
    
    def set_CR(self, CR_probs, CR_vals):
        """Select crossover value for a given iteration.

        Parameters
        ----------
        CR_probs : numpy array
            current probabilities of selecting given crossover values
        CR_values : numpy array
            possible crossover values"""
        CR_loc = np.where(np.random.multinomial(1, CR_probs) == 1)

        CR = CR_vals[CR_loc]
        
        return CR
    
    def set_DEpair(self, DEpairs):
        """Select the number of pairs of chains to be used for creating the next proposal point for a given iteration.

        Parameters
        ----------
        DEpairs : numpy array
            possible values for the number of chain pairs to be used for proposing the next point"""

        if len(DEpairs) > 1:
            DEpair_choice = np.squeeze(np.random.randint(1, len(DEpairs) + 1, size=1))
        else:
            DEpair_choice = 1
        return DEpair_choice
    
    def set_gamma_level(self, gamma_level_probs, gamma_level_vals):
        """Set gamma level value given current probabilities and possible values.

        Parameters
        ----------
        gamma_level_probs : numpy array
            current probabilities of selecting possible gamma levels
        gamma_level_vals : numpy array
            possible values of gamma level"""

        gamma_loc = np.where(np.random.multinomial(1, gamma_level_probs) == 1)
        
        gamma_level = np.squeeze(gamma_level_vals[gamma_loc])
        
        return gamma_level
    
    def set_gamma(self, DEpairs, snooker_choice, gamma_level_choice, d_prime):
        """Select gamma value for a given iteration.

        Parameters
        ----------
        DEpairs : int
            selected number of chain pairs to be used for proposing the next point
        snooker_choice : bool
            whether to use a snooker update scheme on this iteration
        gamma_level_choice : int
            selected level of gamma values to be used this iteration
        d_prime : int
            number of parameter dimensions to be updated on this step."""
        
        gamma_unity_choice = np.where(np.random.multinomial(1, [self.p_gamma_unity, 1 - self.p_gamma_unity]) == 1)
        
        if snooker_choice:
            gamma = np.random.uniform(1.2, 2.2)
            
        elif gamma_unity_choice[0] == 0:
            gamma = 1.0
        
        else:
            gamma = self.gamma_arr[gamma_level_choice - 1][DEpairs - 1][d_prime - 1]
            
        return gamma

    def draw_from_prior(self, model_vars, random_seed=False):
        """Draw from a parameter's prior to seed history array.

        Parameters
        ----------
        model_vars : iterable of instance(s) of SampledParam class
            Model parameters to be sampled with their previously specified prior
        """
        
        draw = np.array([])
        for variable in model_vars:
            try:
                var_draw = variable.random(reseed=random_seed)
            except AttributeError:
                raise Exception('Random draw from distribution for variable %s not implemented yet.' % variable)
            draw = np.append(draw, var_draw)
        return draw.flatten()

    def sample_from_history(self, nseedchains, DEpairs, ndimensions, snooker=False):
        """Draw random point from the history array.

        Parameters
        ----------
        nseedchains : int
            number of points with which the history was initially seeded
        DEpairs : int
            number of pairs of chains to be used for proposing the next point
        ndimensions : int
            number of dimensions in a draw
        snooker : bool
            whether to use a snooker update at this iteration. Default = False
        """

        # To avoid sample unwritten history
        nanflag = True
        while nanflag:
            if not snooker:
                chain_num = random.sample(range(int(self.global_count + nseedchains)), DEpairs * 2)
            else:
                chain_num = random.sample(range(int(self.global_count + nseedchains)), 1)
            start_locs = [int(i * ndimensions) for i in chain_num]
            end_locs = [int(i + ndimensions) for i in start_locs]
            sampled_chains = [Dream_shared_vars.history[start_loc:end_loc] for start_loc, end_loc in zip(start_locs, end_locs)]
            if not np.any(np.isnan(sampled_chains)):
                nanflag = False
        return sampled_chains
        
    def generate_proposal_points(self, n_proposed_pts, q0, CR, DEpairs, gamma_level, snooker):
        """Generate proposal points.

        Parameters
        ----------
        n_proposed_pts : int
            Number of points to propose this iteration (greater than one if using multi-try update scheme)
        q0 : numpy array
            Original point in parameter space
        CR : float
            Crossover value selected for this iteration
        DEpairs : int
            Number of chain pairs to use for proposing the next point for this iteration
        gamma_level : int
            Level of gamma values to use for this iteration
        snooker : bool
            Whether to use a snooker update on this iteration."""

        if not snooker:
            
            sampled_history_pts = np.array([self.sample_from_history(self.nseedchains, DEpairs, self.total_var_dimension) for i in range(n_proposed_pts)])

            chain_differences = np.array([np.sum(sampled_history_pts[i][0:DEpairs], axis=0)-np.sum(sampled_history_pts[i][DEpairs:DEpairs*2], axis=0) for i in range(len(sampled_history_pts))])

            zeta = np.array([np.random.normal(0, self.zeta, self.total_var_dimension) for i in range(n_proposed_pts)])

            e = np.array([np.random.uniform(-self.lamb, self.lamb, self.total_var_dimension) for i in range(n_proposed_pts)])
            e = e+1

            d_prime = self.total_var_dimension
            U = np.random.uniform(0, 1, size=chain_differences.shape)
            
            #Select gamma values given number of parameter dimensions to be changed (d_prime).
            if n_proposed_pts > 1:
                d_prime = [len(U[point][np.where(U[point]<CR)]) for point in range(n_proposed_pts)]
                self.gamma = [self.set_gamma(DEpairs, snooker, gamma_level, d_p) for d_p in d_prime]

                
            else:
                d_prime = len(U[np.where(U<CR)])
                self.gamma = self.set_gamma(DEpairs, snooker, gamma_level, d_prime)
                
            #Generate proposed points given gamma values.
            if n_proposed_pts > 1:
                proposed_pts = [q0 + e[point]*gamma*chain_differences[point] + zeta[point] for point, gamma in zip(range(n_proposed_pts), self.gamma)]

            else:
                proposed_pts = q0+ e*self.gamma*chain_differences + zeta             
                
            #Crossover proposed points based on number of parameter dimensions to be changed.
            if np.any(d_prime != self.total_var_dimension):
                if n_proposed_pts > 1:
                    for point, pt_num in zip(proposed_pts, range(n_proposed_pts)):
                        proposed_pts[pt_num][np.where(U[pt_num]>CR)] = q0[np.where(U[pt_num]>CR)]

                else:
                    proposed_pts[np.where(U>CR)] = q0[np.where(U>CR)[1]] 

        else:
            #With a snooker update all CR always equals 1 (i.e. all parameter dimensions are changed).
            self.gamma = self.set_gamma(DEpairs, snooker, gamma_level, self.total_var_dimension)
            proposed_pts, snooker_logp, z = self.snooker_update(n_proposed_pts, q0)

        #If uniform priors were used, check that proposed points are within bounds and reflect if not.
        if self.boundaries:
            if n_proposed_pts > 1:
                for pt_num in range(n_proposed_pts):
                    masked_point = proposed_pts[pt_num][self.boundary_mask]
                    x_lower = masked_point < self.mins
                    x_upper = masked_point > self.maxs
                    if x_lower.any():
                        masked_point[x_lower] = 2 * self.mins[x_lower] - masked_point[x_lower]
                    if x_upper.any():
                        masked_point[x_upper] = 2 * self.maxs[x_upper] - masked_point[x_upper]
                   
                    #Occasionally reflection will result in points still outside of boundaries
                    x_lower = masked_point < self.mins
                    x_upper = masked_point > self.maxs
                    if x_lower.any():
                        masked_point[x_lower] = self.mins[x_lower] + np.random.rand(len(np.where(x_lower==True)[0])) * (self.maxs[x_lower]-self.mins[x_lower])
                    if x_upper.any():
                        masked_point[x_upper] = self.mins[x_upper] + np.random.rand(len(np.where(x_upper==True)[0])) * (self.maxs[x_upper]-self.mins[x_upper])

                    proposed_pts[pt_num][self.boundary_mask] = masked_point
                   
            else:
                masked_point = np.squeeze(proposed_pts)[self.boundary_mask]

                x_lower = masked_point < self.mins
                x_upper = masked_point > self.maxs

                if x_lower.any():
                    masked_point[x_lower] = 2 * self.mins[x_lower] - masked_point[x_lower]

                if x_upper.any():
                    masked_point[x_upper] = 2 * self.maxs[x_upper] - masked_point[x_upper]
               
                #Occasionally reflection will result in points still outside of boundaries
                x_lower = masked_point < self.mins
                x_upper = masked_point > self.maxs

                if x_lower.any():
                    masked_point[x_lower] = self.mins[x_lower] + np.random.rand(len(np.where(x_lower==True)[0])) * (self.maxs[x_lower]-self.mins[x_lower])
                if x_upper.any():
                    masked_point[x_upper] = self.mins[x_upper] + np.random.rand(len(np.where(x_upper==True)[0])) * (self.maxs[x_upper]-self.mins[x_upper])
                if not snooker:
                    try:
                        proposed_pts[0][self.boundary_mask] = masked_point

                    except IndexError:
                        #Raised in the unusual case when total variable dimension = 1
                        if self.boundary_mask:
                            proposed_pts = np.array([masked_point])
                else:
                    try:
                        proposed_pts[self.boundary_mask] = masked_point

                    except IndexError:
                        #Raised in the unusual case when total variable dimension = 1
                        if self.boundary_mask:
                            proposed_pts = np.array([masked_point])

        if not snooker:
            return proposed_pts
        else:
            return proposed_pts, snooker_logp, z
        
    def snooker_update(self, n_proposed_pts, q0):
        """Generate a proposed point with snooker updating scheme.

        Parameters
        ----------
        n_proposed_pts : int
            Number of points to propose this iteration (greater than one if using multi-try update scheme)
        q0 : numpy array
            Original point in parameter space"""
        
        sampled_history_pt = [self.sample_from_history(self.nseedchains, self.DEpairs, self.total_var_dimension, snooker=True) for i in range(n_proposed_pts)]

        chains_to_be_projected = np.squeeze([np.array([self.sample_from_history(self.nseedchains, self.DEpairs, self.total_var_dimension, snooker=True) for i in range(2)]) for x in range(n_proposed_pts)])

        #Define projection vector
        proj_vec_diff = np.squeeze(q0-sampled_history_pt)

        if n_proposed_pts > 1:
            D = [np.dot(proj_vec_diff[point], proj_vec_diff[point]) for point in range(len(proj_vec_diff))]
            
            #Orthogonal projection of chains_to_projected onto projection vector
            diff_chains_to_be_projected = [(chains_to_be_projected[point][0]-chains_to_be_projected[point][1]) for point in range(n_proposed_pts)]       
            zP = np.nan_to_num(np.array([(np.sum(diff_chains_to_be_projected[point]*proj_vec_diff[point])/D[point] *proj_vec_diff[point]) for point in range(n_proposed_pts)]))
            dx = self.gamma*zP
            proposed_pts = [q0 + dx[point] for point in range(n_proposed_pts)]
            norms = [np.linalg.norm(proposed_pts[point] - sampled_history_pt[point]) for point in range(n_proposed_pts)]
            snooker_logp = [np.log(norm, where= norm != 0)*(self.total_var_dimension-1) for norm in norms]

        else:
            D = np.dot(proj_vec_diff, proj_vec_diff)

            #Orthogonal projection of chains_to_projected onto projection vector  
            diff_chains_to_be_projected = chains_to_be_projected[0]-chains_to_be_projected[1]
            zP = np.nan_to_num(np.array([np.sum(np.divide((diff_chains_to_be_projected*proj_vec_diff), D, where= D != 0))]))*proj_vec_diff
            dx = self.gamma*zP
            proposed_pts = q0 + dx
            norm = np.linalg.norm(proposed_pts-sampled_history_pt)
            snooker_logp = np.log(norm, where= norm != 0)*(self.total_var_dimension-1)
        
        return proposed_pts, snooker_logp, sampled_history_pt
    
    def mt_evaluate_logps(self, parallel, multitry, proposed_pts, pfunc, ref=False):
        """Evaluate the log probability for multiple points in serial or parallel when using multi-try.

        Parameters
        ----------
        parallel : bool
            Whether to evaluate multi-try points in parallel
        multitry : int
            Number of multi-try points
        proposed_pts : numpy 2D array nmulti-try x nparameterdims
            Proposed points
        pfunc : function
            Function that takes a point in parameter space and
            returns the log of the prior value and the log of the likelihood at that point
        ref : bool
            Whether this is a multi-try reference draw. Default = False"""
        
        #If using multi-try and running in parallel farm out proposed points to process pool.
        if parallel:
            args = list(zip([self] * multitry, np.squeeze(proposed_pts)))
            with pool.Pool(multitry, context=self.mp_context) as p:
                logps = p.map(call_logp, args)
            log_priors = [val[0] for val in logps]
            log_likes = [val[1] for val in logps]
            
        else:
            log_priors = []
            log_likes = []
            if multitry == 2:
                log_priors, log_likes = np.array([pfunc(np.squeeze(proposed_pts))])
            else:
                for pt in np.squeeze(proposed_pts):
                    log_priors.append(pfunc(pt)[0])  
                    log_likes.append(pfunc(pt)[1])
        
        log_priors = np.array(log_priors)  
        log_likes = np.array(log_likes)
        
        if ref:
            log_likes = np.append(log_likes, self.last_like)
            log_priors = np.append(log_priors, self.last_prior)
            
        return log_priors, log_likes

    def mt_choose_proposal_pt(self, log_priors, log_likes, proposed_pts, T):
        """Select a proposed point with probability proportional to the probability density at that point.

        Parameters
        ----------
        log_priors : numpy array
            Values of the log prior probability for all proposed multi-try points
        log_likes : numpy array
            Values of the log likelihood probability for all proposed multi-try points
        proposed_pts : numpy 2D array nmulti-tries x nparameterdims
            Proposed points
        T : float
            Temperature (only used if using parallel tempering)"""
        
        #Substract largest logp from all logps (this from original Matlab code)
        org_log_likes = log_likes
        log_likes = T * log_likes
        log_ps = log_priors + log_likes
        noT_logps = org_log_likes + log_priors
        max_logp = np.amax(log_ps)
        log_ps_sub = np.exp(log_ps - max_logp)

        #Calculate probabilities
        sum_proposal_logps = np.sum(log_ps_sub)
        logp_prob = log_ps_sub/sum_proposal_logps
        best_logp_loc = int(np.squeeze(np.where(np.random.multinomial(1, logp_prob)==1)[0]))

        #Randomly select one of the tested points with probability proportional to the probability density at the point
        q_proposal = np.squeeze(proposed_pts[best_logp_loc])
        q_logp = log_ps[best_logp_loc] 
        q_prior = log_priors[best_logp_loc]
        noT_loglike = org_log_likes[best_logp_loc]
        noT_logp = noT_logps[best_logp_loc]
        
        return q_proposal, q_logp, noT_logp, noT_loglike, q_prior
        
    def record_history(self, nseedchains, ndimensions, q_new, len_history):
        """Record accepted point in history.

        Parameters
        ----------
        nseedchains : int
            Number of points in parameter space with which the original history was seeded
        ndimensions : int
            Number of parameter dimensions being sampled
        q_new : numpy array
            Accepted point
        len_history : int
            The total dimension of the history when completely filled"""
        """
        one = np.array([1], dtype='i')
        recv_buf = np.zeros(1, dtype='i')       
        self.counter_win.Lock(0)
        self.counter_win.Fetch_and_op(
            [one, 1, MPI.INT],    
            [recv_buf, 1, MPI.INT],
            target_rank=0,        
            op=MPI.SUM       
        )
        self.counter_win.Unlock(0)

        local_index = recv_buf[0]
        nhistoryrecs = local_index + nseedchains
        start_loc = int(nhistoryrecs * ndimensions)
        end_loc = int(start_loc + ndimensions)
        

        Dream_shared_vars.history[start_loc:end_loc] = np.array(q_new).flatten()
        self.local_count += 1
        """
 

        self.global_count = self.local_count * self.nchains + self.chainID
        nhistoryrecs = self.global_count + nseedchains
        start_loc = int((nhistoryrecs) * ndimensions)
        end_loc = int(start_loc + ndimensions)


        #Dream_shared_vars.win_history.Lock(0)
        #Dream_shared_vars.win_history.Lock(lock_type=MPI.LOCK_SHARED, rank=0)
        Dream_shared_vars.win_history.Get(Dream_shared_vars.history, target_rank=0, target=0)  # Pull the whole array
        Dream_shared_vars.win_history.Put(
                np.array(q_new).flatten(),  # local data
                target_rank=0,  # rank to write
                target=start_loc * q_new.dtype.itemsize
            )
        #Dream_shared_vars.win_history.Unlock(0)
        Dream_shared_vars.win_history.Fence()
        #Dream_shared_vars.win_history.Flush(0)
        #print(self.chainID, np.sum(np.isnan(Dream_shared_vars.history)), flush=True)

        #start_loc1 = int (((self.local_count-1) * self.nchains  + self.chainID + nseedchains) * ndimensions)
        #end_loc1 = int(start_loc1 + ndimensions)
        #print(start_loc, end_loc, start_loc1, end_loc1, q_new.flatten()[:5], Dream_shared_vars.history[start_loc:end_loc][:5], Dream_shared_vars.history[start_loc1:end_loc1][:5], flush=True) # todo
        #print(self.local_count * self.nchains, nseedchains, ndimensions, start_loc1, flush=True)
        #print(self.local_count, self.chainID, start_loc, end_loc, q_new[:3], Dream_shared_vars.history[start_loc:end_loc][:3],  start_loc1, end_loc1, Dream_shared_vars.history[start_loc1:end_loc1][:3], flush=True)

        self.local_count += 1

        #if self.save_history and len_history == (nhistoryrecs+1)*ndimensions:
        """
        if self.save_history and self.iter == (self.niterations - 1):
            #if not (np.any(np.isnan(Dream_shared_vars.history))):
            try:
                if not self.model_name:
                    prefix = datetime.now().strftime('%Y_%m_%d_%H:%M:%S')+'_'
                else:
                    prefix = self.model_name+'_'
                    self.save_history_to_disc(Dream_shared_vars.history, prefix)
            except:
                pass
        """        
                
        
        return self.global_count
            
    def save_history_to_disc(self, history, prefix):
        """Save history and crossover probabilities to files at end of run.

        Parameters
        ----------
        history : numpy array
            History array
        prefix : str
            Prefix to add to history filename when saving"""
        
        filename = prefix+'DREAM_chain_history.npy'
        print('Rank ', self.chainID, ' :   Saving history to file: ', os.getcwd() + filename)
        np.save(filename, history)
        
        #Also save crossover probabilities if adapted
        filename = prefix+'DREAM_chain_adapted_crossoverprob.npy'
        print('Saving fitted crossover values: ',self.CR_probabilities,' to file: ',filename)
        np.save(filename, self.CR_probabilities)
        
        #Also save gamma level probabilities
        filename = prefix+'DREAM_chain_adapted_gammalevelprob.npy'
        print('Saving fitted gamma level values: ',self.gamma_probabilities,' to file: ',filename)
        np.save(filename, self.gamma_probabilities)
    
def call_logp(args):
    #Defined at top level so it can be pickled.
    instance = args[0]
    tested_point = args[1]
    
    logp_fxn = getattr(instance, 'logp')
    
    return logp_fxn(tested_point)
    
def metrop_select(mr, q, q0):
    """Perform Metropolis rejection/acceptance

    Parameters
    ----------
    mr : float
        Metropolis ratio
    q : numpy array
        Proposed point
    q0 : numpy array
        Original point"""


    # Compare acceptance ratio to uniform random number
    if np.isfinite(mr) and np.log(np.random.uniform()) < mr:
        # Accept proposed value
        return q
    else:
        # Reject proposed value
        return q0