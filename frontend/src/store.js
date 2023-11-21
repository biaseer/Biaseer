import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	displayMode: 'vis',
    // Specify the current media in order to display a feature trend view; 
    // Ultimately, it can be replaced with a global feature trend view.
    currMedium: 'msn.com',
    mediaMatrixSelectedSignal: 1, // signal media matrix selected

    storytree_finish: 0,

    mediaScatterClick: 0,

    mediaGraphLabel: 0,

    mediaDiffConcatSignal: 0,
    concatdiff_finish: 0,
    
    tree_node_click: null,
    tree_node_circle_click: -1,
    tree_node_circle_click_path_list: null,

    isConcated: false,
    
    clickSankeyTreeNode: 0,

    contour_search_domain: '',
  },
  mutations: {
    ['UPDATE_CONTOUR_SEARCH_DOMAIN'] (state, contour_search_domain) {
      // console.log("contour_search_domain",contour_search_domain)
      state.contour_search_domain = contour_search_domain
    },
    ['UPDATE_CLICK_SANKEY_TREE_NODE_MODE'] (state) {
      // console.log("点击了一个节点")
      state.clickSankeyTreeNode = (state.clickSankeyTreeNode + 1 ) % 5;
    },

    ['UPDATE_DISPLAY_MODE'] (state, displayMode) {
      state.displayMode = displayMode;
    },
    
    ['UPDATE_CURRENT_MEDIUM'] (state, currMedium) {
      console.log(currMedium);
      state.currMedium = currMedium;
    },
    
    ['UPDATE_MATRIX_SELECTED_SIGNAL'] (state) {
      console.log(state.mediaMatrixSelectedSignal);
      state.mediaMatrixSelectedSignal = (state.mediaMatrixSelectedSignal + 1) % 5;
    },

    ['UPDATE_STORYTREE_FINISH'](state){
      state.storytree_finish = (state.storytree_finish + 1 ) % 5;
    },

    ['UPDATE_MEDIA_SCATTER_CLICK'](state){
      state.mediaScatterClick = (state.mediaScatterClick + 1 ) % 5;
    },

    ['UPDATE_MEDIA_GRAPH_LABEL'](state){
      state.mediaGraphLabel = (state.mediaGraphLabel + 1 ) % 5;
    },

    ['UPDATE_MEDIA_DIFF_CONCAT_SIGNAL'](state){
      state.mediaDiffConcatSignal = (state.mediaDiffConcatSignal + 1 ) % 5;
    },

    ['UPDATE_CONCATDIFF_FINISH'](state){
      state.concatdiff_finish = (state.concatdiff_finish + 1 ) % 5;
    },

    ['UPDATE_TREE_NODE_CLICK_PATH_LIST'] (state, tree_node_circle_click_path_list) {
      console.log("tree_node_circle_click_path_list",tree_node_circle_click_path_list)
      state.tree_node_circle_click_path_list = tree_node_circle_click_path_list
    },

    ['UPDATE_TREE_NODE_CLICK'] (state, tree_node_click) {
      state.tree_node_click = tree_node_click
    },

    ['UPDATE_CONCAT_STATUS'] (state, isConcated) {
      state.isConcated = isConcated;
    },
  },
  actions: {
  }
})
