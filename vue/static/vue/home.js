window.onload = function(){
    // set current viewing page as page_type and call populate

    // OR STORE PAGE_TYPE in localstorage so that it will be available even after reload

}

var mainApp = new Vue({
    el: '#mainApp',
    delimiters: ['[[',']]'],
    data:{
        // menu bar
        loggedin_user : localStorage.loggedin_user,
        page_type : 'home',
        searchbar_input : '',

        // POST photo
        upload_image : '',
        upload_hashtags : '',

        // GET photos
        search_results : [],
        main_data : [],
        
        // like and comment data
        upload_comment : '',
        all_likes : [],
        all_comments : [],
        likeModalPopup : false,
        CommentModalPopup : false,
    },
    beforeMount: function(){
            if(!this.loggedin_user){
                window.location = '/login/';
            }
            this.setPageType('home');
    },
    methods: {
                // MENU buttons click handler
                setPageType(t){
                    this.populate(t,null);
                },
                
                // upload Photopost (from my profile)
                loadUploadImage(e){
                    this.upload_image = e.target.files[0];
                },
                async uploadPhotopost(){
                    var url = api_url+'photopost/create/';
                    var headers = new Headers();
                    headers.append('Authorization','Token '+localStorage.auth_token);
                    var formData = new FormData();
                    formData.append('image',this.upload_image);
                    formData.append('hashtags',this.upload_hashtags);
                    var request = new Request(url, {method:'POST',headers,body:formData});
                    resp = await fetch(request);
                    data = await resp.json();
                    this.populate('myprofile',null);
                },

                // Delete Photopost (from my profile)
                async deletePhotopost(i){
                    var val = confirm("Delete this post?");
                    if(val == true ){
                        var url = api_url + 'photopost/delete/'+i.id;
                        var headers = new Headers();
                        headers.append('Authorization','Token '+localStorage.auth_token);
                        var request = new Request(url,  {  method:'DELETE',headers }   );
                        resp = await fetch(request);
                        data = await resp.json();
                        this.populate('myprofile',null);
                    }
                },
                
                // goto friend page
                async gotoFriendPage(username){
                    this.CommentModalPopup = false;
                    this.likeModalPopup = false;
                    this.populate('friend',username);
                },

                // get Photoposts wrt page_type
                async populate(p_type,username){
                    var url = '';
                    if(p_type == 'home'){
                        url = api_url+'home-feed/';
                    }
                    else if(p_type == 'myprofile'){
                        url = api_url+'getuserposts/'+localStorage.loggedin_user;
                    }
                    else if(p_type == 'friend'){
                        url = api_url + 'getuserposts/'+ username;
                    }
                    else if(p_type  ==  'search'){
                        url = api_url+'search/'+this.searchbar_input;
                    }
                    else{
                        return;
                    }
                    this.page_type = p_type;
                
                    var headers = new Headers();
                    headers.append('Authorization','Token '+localStorage.auth_token);
                    var request = new Request(url,  {  method:'GET',headers }   );
                    resp = await fetch(request);
                    data = await resp.json();

                    if(this.page_type=='search'){
                        this.search_results = await data;
                        this.main_data = [];
                    }else{
                        this.search_results = [];
                        this.main_data = await data;
                    }
                },

                
                // like Photopost
                async likePhoto(i){
                    var url = api_url+'like/'+i.id;
                    var headers = new Headers();
                    headers.append('Authorization','Token '+localStorage.auth_token);
                    var request = new Request(url, {method:'POST',headers});
                    resp = await fetch(request);
                    data = await resp.json();
                    if(data.response == 'liked')
                        i.is_liked = true;
                    else
                        i.is_liked = false;
                },
                async getAllLikes(i){
                    var url = api_url + 'getlikes/'+i.id;
                    var headers = new Headers();
                    headers.append('Authorization','Token '+localStorage.auth_token);
                    var request = new Request(url,  {  method:'GET',headers }   );
                    resp = await fetch(request);
                    this.all_likes = await resp.json();
                    this.likeModalPopup = true;
                },

                // comment Photopost
                async commentPhoto(i){
                    var url = api_url+'comment/'+i.id;
                    var headers = new Headers();
                    headers.append('Authorization','Token '+localStorage.auth_token);
                    var formData = new FormData();
                    formData.append('comment',this.upload_comment);
                    var request = new Request(url, {method:'POST',headers, body:formData});
                    resp = await fetch(request);
                    data = await resp.json();
                    this.upload_comment = '';
                },
                async deleteComment(i){
                    var url = api_url + 'comment/delete/'+i.id;
                    var headers = new Headers();
                    headers.append('Authorization','Token '+localStorage.auth_token);
                    var request = new Request(url,  {  method:'DELETE',headers }   );
                    resp = await fetch(request);
                    data = await resp.json();
                    
                    // remove from all_comments data
                    var index = this.all_comments.indexOf(i);
                    this.all_comments.splice(index, 1);
                },
                async getAllComments(i){
                    var url = api_url + 'getcomments/'+i.id;
                    var headers = new Headers();
                    headers.append('Authorization','Token '+localStorage.auth_token);
                    var request = new Request(url,  {  method:'GET',headers }   );
                    resp = await fetch(request);
                    this.all_comments = await resp.json();
                    this.CommentModalPopup = true;
                },
    },
});
